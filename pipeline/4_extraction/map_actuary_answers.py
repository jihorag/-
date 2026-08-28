import json
import os
import fitz
import re
import shutil
import unicodedata

DB_PATH = "questions_db.json"
BASE_DIR = "sources/기출문제/보험계리사"

def norm(s):
    return unicodedata.normalize("NFC", s)

def get_answer_pdfs():
    answer_files = []
    abs_base = os.path.abspath(BASE_DIR)
    for root, dirs, files in os.walk(abs_base):
        for f in files:
            f_norm = norm(f)
            if "답안" in f_norm or "정답" in f_norm:
                root_norm = norm(root)
                year_match = re.search(r"20\d{2}", root_norm)
                if year_match:
                    year = year_match.group()
                    answer_files.append({
                        "year": year,
                        "path": os.path.join(root, f)
                    })
    return answer_files

def extract_answers_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()

    lines = [l.strip() for l in full_text.split("\n") if l.strip()]
    results = {"경제학": {}, "회계원리": {}}
    
    found_rows = []
    for i, line in enumerate(lines):
        if line.isdigit():
            num = int(line)
            if 1 <= num <= 40:
                row = [num]
                j = 1
                # Try to grab next 6 columns (Ans1-6)
                while i + j < len(lines) and lines[i+j].isdigit() and len(lines[i+j]) == 1:
                    row.append(int(lines[i+j]))
                    j += 1
                if len(row) >= 5:
                    found_rows.append(row)

    for row in found_rows:
        num = row[0]
        if len(row) >= 5:
            results["경제학"][num] = str(row[4])
        if len(row) >= 7:
            results["회계원리"][num] = str(row[6])

    return results

def main():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    answer_pdfs = get_answer_pdfs()
    all_answers = {}
    for ap in answer_pdfs:
        year = ap["year"]
        ans = extract_answers_from_pdf(ap["path"])
        if year not in all_answers: all_answers[year] = ans
        else:
            all_answers[year]["경제학"].update(ans["경제학"])
            all_answers[year]["회계원리"].update(ans["회계원리"])

    updated_count = 0
    for q in db:
        q_id = q.get("id", "")
        if "actuary" not in q_id:
            continue
            
        year = str(q.get("year"))
        subject = q.get("subject", "")
        number = int(q.get("number", 0)) # Convert string number to int for matching
        
        if year in all_answers:
            subject_key = None
            if "경제" in subject: subject_key = "경제학"
            elif "회계" in subject: subject_key = "회계원리"
            
            if subject_key and number in all_answers[year][subject_key]:
                q["answer"] = all_answers[year][subject_key][number]
                updated_count += 1

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    shutil.copy(DB_PATH, "viewer/src/data/questions_db.json")
    print(f"Successfully updated {updated_count} answers.")

if __name__ == "__main__":
    main()
