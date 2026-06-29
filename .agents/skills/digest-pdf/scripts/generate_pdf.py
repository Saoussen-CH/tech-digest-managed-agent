#!/usr/bin/env python3
"""Generate /workspace/digest.pdf from /workspace/summaries.json."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SUMMARIES_PATH = Path("/workspace/summaries.json")
PDF_PATH = Path("/workspace/digest.pdf")


def ensure_reportlab():
    try:
        import reportlab  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])


def main():
    if not SUMMARIES_PATH.exists():
        print(f"ERROR: {SUMMARIES_PATH} not found. Write summaries.json first.", file=sys.stderr)
        sys.exit(1)

    ensure_reportlab()

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

    data = json.loads(SUMMARIES_PATH.read_text())

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("DigestTitle", parent=styles["Title"], fontSize=24, spaceAfter=6)
    date_style = ParagraphStyle("DigestDate", parent=styles["Normal"], fontSize=11,
                                textColor=colors.grey, spaceAfter=20)
    source_style = ParagraphStyle("SourceHead", parent=styles["Heading2"],
                                  fontSize=14, spaceBefore=16, spaceAfter=8)
    story_title_style = ParagraphStyle("StoryTitle", parent=styles["Normal"],
                                       fontSize=11, fontName="Helvetica-Bold", spaceAfter=4)
    summary_style = ParagraphStyle("StorySummary", parent=styles["Normal"],
                                   fontSize=10, leading=14, spaceAfter=12)

    date_str = data.get("date", datetime.today().strftime("%Y-%m-%d"))

    elements = [
        Paragraph("Daily Tech Digest", title_style),
        Paragraph(date_str, date_style),
        HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=16),
    ]

    for source in data.get("sources", []):
        elements.append(Paragraph(source["name"], source_style))
        for item in source.get("stories", []):
            elements.append(Paragraph(item["title"], story_title_style))
            elements.append(Paragraph(item["summary"], summary_style))

    doc.build(elements)
    size = PDF_PATH.stat().st_size
    print(f"Saved {PDF_PATH} ({size:,} bytes)")


if __name__ == "__main__":
    main()
