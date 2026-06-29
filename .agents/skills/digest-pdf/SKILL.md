---
name: digest-pdf
description: Fetch tech headlines, write editorial summaries, and generate a formatted PDF at /workspace/digest.pdf
---

## Steps

1. Fetch the front page of each source using url_context or run_code with requests:
   - https://news.ycombinator.com
   - https://techcrunch.com
   - https://theverge.com

2. Select the top 5 stories per source (15 total). Skip duplicates across sources.

3. For each story write a 2-3 sentence editorial summary in the configured voice.

4. Save all summaries to /workspace/summaries.json in this exact format:
   {
     "date": "YYYY-MM-DD",
     "sources": [
       {
         "name": "Hacker News",
         "url": "https://news.ycombinator.com",
         "stories": [
           {"title": "Story title", "summary": "2-3 sentence editorial summary."}
         ]
       }
     ]
   }

5. Run the PDF generator script:
   python .agents/skills/digest-pdf/scripts/generate_pdf.py

6. Confirm the file exists:
   ls -lh /workspace/digest.pdf

## Rules
- Always write summaries.json before running the script. Never generate an empty PDF.
- If a source is unreachable, skip it and include a note in summaries.json.
- The PDF must be at exactly /workspace/digest.pdf.
