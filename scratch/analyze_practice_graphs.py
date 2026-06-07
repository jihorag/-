import os
import json
import glob

def analyze():
    base_dir = "/Users/hanjiho/Documents/감정평가사 기출문제/viewer/public/data/practice/economics"
    pattern = os.path.join(base_dir, "micro-ch*.json")
    files = sorted(glob.glob(pattern))
    
    print(f"{'File Name':<35} | {'Total Q':<7} | {'With SVG':<8} | {'SVG %':<6} | L1 | L2 | L3 | L4 | L5")
    print("-" * 90)
    
    grand_total_q = 0
    grand_total_svg = 0
    grand_diff_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
            
        questions = data.get("questions", [])
        total_q = len(questions)
        svg_q = 0
        diff_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for q in questions:
            diff = q.get("difficulty", 3)
            diff_dist[diff] = diff_dist.get(diff, 0) + 1
            
            # Check for svg in question text
            q_text = q.get("question", "")
            if "```svg" in q_text or "<svg" in q_text:
                svg_q += 1
                
        grand_total_q += total_q
        grand_total_svg += svg_q
        for k in range(1, 6):
            grand_diff_dist[k] += diff_dist[k]
            
        svg_pct = (svg_q / total_q * 100) if total_q > 0 else 0
        diff_str = " | ".join(f"{diff_dist[k]:<2}" for k in range(1, 6))
        print(f"{filename:<35} | {total_q:<7} | {svg_q:<8} | {svg_pct:>5.1f}% | {diff_str}")
        
    print("-" * 90)
    grand_svg_pct = (grand_total_svg / grand_total_q * 100) if grand_total_q > 0 else 0
    grand_diff_str = " | ".join(f"{grand_diff_dist[k]:<2}" for k in range(1, 6))
    print(f"{'GRAND TOTAL':<35} | {grand_total_q:<7} | {grand_total_svg:<8} | {grand_svg_pct:>5.1f}% | {grand_diff_str}")

if __name__ == "__main__":
    analyze()
