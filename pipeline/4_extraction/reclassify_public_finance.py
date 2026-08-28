import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

TAXONOMY = [
    "1장 재정학의 기초 및 후생경제학",
    "2장 공공재이론",
    "3장 외부성",
    "4장 공공선택이론",
    "5장 비용편익분석",
    "6장 조세이론의 기초",
    "7장 조세의 경제적 효과",
    "8장 최적조세이론",
    "9장 개별 조세론 (소득세, 법인세 등)",
    "10장 소득분배 및 사회보장",
    "11장 지방재정 및 공공채무"
]

def reclassify_batch(batch_data):
    client = genai.Client(api_key=gemini_api_key)
    
    prompt = f"""
다음은 세무사 재정학 기출문제들의 정보(ID, 문제내용 요약, 핵심개념)입니다.
이 문제들을 아래의 **재정학 표준 단원 분류(1장~11장)** 중 가장 적합한 곳으로 하나씩 매칭해 주세요.

[표준 단원 분류]
{chr(10).join(TAXONOMY)}

[문제 데이터]
{json.dumps(batch_data, ensure_ascii=False, indent=2)}

[응답 형식]
반드시 아래 JSON 객체 형식으로만 응답하세요 (키는 문제 ID, 값은 선택한 장 이름):
{{
  "tax_2026_재정학_1": "1장 재정학의 기초 및 후생경제학",
  ...
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error in batch: {e}")
        return {}

def main():
    db_path = 'questions_db.json'
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)

    target_questions = []
    for q in db:
        if q.get('subject') == '재정학':
            target_questions.append({
                "id": q['id'],
                "text": q.get('question', '')[:100],
                "concept": q.get('tags', {}).get('concept', '')
            })

    print(f"Total target questions: {len(target_questions)}")
    
    mapping = {}
    batch_size = 30
    for i in range(0, len(target_questions), batch_size):
        batch = target_questions[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} / {len(target_questions)//batch_size + 1}...")
        res = reclassify_batch(batch)
        mapping.update(res)

    # Apply mapping
    count = 0
    for q in db:
        if q['id'] in mapping:
            if 'tags' not in q: q['tags'] = {}
            q['tags']['subject'] = '경제학'
            q['tags']['unit'] = 'PART 003 재정학'
            q['tags']['sub_unit'] = mapping[q['id']]
            count += 1

    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    with open('viewer/src/data/questions_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Successfully updated {count} questions.")

if __name__ == "__main__":
    main()
