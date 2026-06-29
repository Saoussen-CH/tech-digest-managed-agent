from dotenv import load_dotenv
from google import genai
from run_digest import BASE_AGENT, AGENTS_MD, SKILL_MD, GENERATE_PDF_PY

load_dotenv()

client = genai.Client()

# Delete existing agent with this ID if it already exists (safe to re-run)
try:
    client.agents.delete(id="my-digest")
    print("Deleted existing my-digest agent.")
except Exception:
    pass

# TODO 1: call client.agents.create() with id="my-digest", base_agent=BASE_AGENT,
# a description, and base_environment with type="remote" and three inline sources:
# AGENTS_MD → .agents/AGENTS.md
# SKILL_MD  → .agents/skills/digest-pdf/SKILL.md
# GENERATE_PDF_PY → .agents/skills/digest-pdf/scripts/generate_pdf.py
raise NotImplementedError("Fill in TODO 1 before running this file.")

print(f"Saved: {agent.id}")

for a in client.agents.list().agents or []:
    print(f"{a.id}: {getattr(a, 'description', '')}")
