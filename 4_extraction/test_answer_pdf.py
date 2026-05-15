import fitz
import os
import json

def preview_answer_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print(f"--- {os.path.basename(pdf_path)} ---")
    print(text[:1000])
    doc.close()

# Sample 2024 answer
preview_answer_pdf("/Users/jiho/감정평가사 기출문제/기출문제/보험계리사/2024/제47회 1차시험 확정답안.pdf")
