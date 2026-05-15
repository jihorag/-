import json
import unicodedata

def normalize_nfc(obj):
    if isinstance(obj, str):
        return unicodedata.normalize('NFC', obj)
    elif isinstance(obj, list):
        return [normalize_nfc(item) for item in obj]
    elif isinstance(obj, dict):
        return {normalize_nfc(k): normalize_nfc(v) for k, v in obj.items()}
    return obj

def main():
    db_paths = ["questions_db.json", "viewer/src/data/questions_db.json"]
    
    for path in db_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 모든 텍스트를 NFC로 정규화
            clean_data = normalize_nfc(data)
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(clean_data, f, ensure_ascii=False, indent=2)
            print(f"✅ {path} 정규화 완료!")
        except Exception as e:
            print(f"❌ {path} 처리 오류: {e}")

if __name__ == "__main__":
    main()
