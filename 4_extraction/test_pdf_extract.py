import fitz
import re
import json

def extract_cpa_2023_acc():
    doc = fitz.open('기출문제/회계사/2023/__03. 회계학(1형)_문제_2023.pdf')
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    # Simple normalization: remove some obvious artifacts
    full_text = full_text.replace('\n', ' ')
    
    # Pattern to find question number followed by choices
    # This is tricky because of the PDF text layout. 
    # Let's try to split by question markers "N. "
    
    questions = []
    for i in range(1, 51):
        next_q = i + 1
        pattern = rf"{i}\.\s*(.*?)(?={next_q}\.\s*|$)"
        match = re.search(pattern, full_text)
        if match:
            q_block = match.group(1)
            # Find options
            opts = []
            for j in range(1, 6):
                next_j = j + 1
                o_markers = ["①", "②", "③", "④", "⑤", "⑥"]
                opt_pattern = rf"{o_markers[j-1]}(.*?)(?={o_markers[j] if j < 5 else '$'})"
                o_match = re.search(opt_pattern, q_block)
                if o_match:
                    opts.append(o_match.group(1).strip())
            questions.append({
                "number": i,
                "options": opts
            })
    
    return questions

if __name__ == "__main__":
    qs = extract_cpa_2023_acc()
    print(json.dumps(qs[:5], ensure_ascii=False, indent=2))
