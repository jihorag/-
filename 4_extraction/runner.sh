#!/bin/bash

echo "Waiting for extract_tax_2024_fix_civil.py to finish..."
while pgrep -f "extract_tax_2024_fix_civil.py" > /dev/null; do
    sleep 10
done

echo "Starting extraction for all remaining 2024-2026 tax accountant exams..."
python3 4_extraction/extract_tax_all_remaining.py > extraction_remaining.log 2>&1 &
echo "Master extraction script started in the background. Check extraction_remaining.log for progress."
