import json
import shutil

def update_cpa_2023_acc_answers():
    answers = [
        3, 5, 4, 2, 1, 4, 1, 2, 3, 2,
        1, 1, 3, 1, 4, 2, 4, 5, 5, 5,
        2, 1, 4, 4, 4, 2, 5, 4, 3, 5,
        3, 2, 5, 4, 3, 5, 1, 3, 3, 2,
        3, 2, 2, 4, 1, 1, 1, 5, 4, 3
    ]
    
    db_path = "questions_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    updated_count = 0
    for q in db:
        if q.get('id', '').startswith('cpa_2023_acc_'):
            q_num = int(q['id'].split('_')[-1])
            if 1 <= q_num <= 50:
                q['answer'] = str(answers[q_num - 1])
                updated_count += 1
                
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    shutil.copy(db_path, "viewer/src/data/questions_db.json")
    print(f"Successfully updated answers for {updated_count} questions.")

if __name__ == "__main__":
    update_cpa_2023_acc_answers()
