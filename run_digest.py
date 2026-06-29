"""
Daily Tech Digest Agent, powered by Managed Agents with the Gemini API.

Build run_digest() step by step through the codelab.
By the end you will have a complete agent that fetches live tech news,
writes editorial summaries, and generates a PDF, with one API call
and no servers, containers, or orchestration code to manage.

Run: python run_digest.py
"""
from pathlib import Path
from dotenv import load_dotenv, set_key

load_dotenv()

BASE_AGENT = "antigravity-preview-05-2026"
BASE_DIR = Path(__file__).resolve().parent

# Agent configuration files, read from .agents/ at startup
AGENTS_MD       = (BASE_DIR / ".agents/AGENTS.md").read_text(encoding="utf-8")
SKILL_MD        = (BASE_DIR / ".agents/skills/digest-pdf/SKILL.md").read_text(encoding="utf-8")
GENERATE_PDF_PY = (BASE_DIR / ".agents/skills/digest-pdf/scripts/generate_pdf.py").read_text(encoding="utf-8")

PROMPT = (
    "Generate today's tech digest and save it as /workspace/digest.pdf. "
    "Follow the digest-pdf skill."
)


def run_stream(stream) -> tuple[str, str]:
    """Process a stream of events, printing progress.

    Returns (environment_id, interaction_id) from the completed event.
    """
    environment_id = None
    interaction_id = None

    for event in stream:
        event_type = getattr(event, "event_type", None)

        if event_type == "interaction.created":
            print("[agent started]", flush=True)

        elif event_type == "step.start":
            step = getattr(event, "step", None)
            if step:
                stype = getattr(step, "type", "")
                name  = getattr(step, "name", "")
                if stype == "function_call" and name:
                    print(f"  [tool] {name}", flush=True)

        elif event_type == "step.delta":
            delta = getattr(event, "delta", None)
            if delta and getattr(delta, "type", "") == "text":
                print(getattr(delta, "text", ""), end="", flush=True)

        elif event_type == "interaction.completed":
            interaction = getattr(event, "interaction", None)
            if interaction:
                environment_id = getattr(interaction, "environment_id", None)
                interaction_id = getattr(interaction, "id", None)

    return environment_id, interaction_id


# ─────────────────────────────────────────────────────────────────────────────
# Build this function through Steps 1-2.
# ─────────────────────────────────────────────────────────────────────────────

def run_digest():
    pass


if __name__ == "__main__":
    run_digest()
