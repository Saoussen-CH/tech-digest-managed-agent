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

PROMPT = (
    "Generate today's tech digest and save it as /workspace/digest.pdf. "
    "Follow the digest-pdf skill."
)


def load_source(relative_path: str) -> str:
    """Read a config file from the .agents/ directory."""
    return (BASE_DIR / relative_path).read_text(encoding="utf-8")


# TODO 2: load AGENTS_MD, SKILL_MD, and GENERATE_PDF_PY using load_source()


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
                args  = getattr(step, "arguments", None)

                if stype == "function_call":
                    name = getattr(step, "name", "")
                    if name:
                        path = None
                        if args:
                            for key in ("path", "directory", "filename"):
                                path = (args.get(key) if isinstance(args, dict)
                                        else getattr(args, key, None))
                                if path:
                                    break
                        label = f" ({path})" if path else ""
                        print(f"  [tool] {name}{label}", flush=True)

                elif stype == "url_context_call":
                    urls = getattr(args, "urls", []) if args else []
                    label = urls[0] if urls else "url"
                    print(f"  [tool] url_context ({label})", flush=True)

                elif stype == "code_execution_call":
                    code = None
                    if args:
                        code = (getattr(args, "code", None)
                                or getattr(args, "input", None)
                                or getattr(args, "source", None))
                    label = code.split("\n")[0][:60] if code else ""
                    print(f"  [tool] run_code ({label})" if label else "  [tool] run_code", flush=True)

                elif stype == "google_search_call":
                    queries = getattr(args, "queries", []) if args else []
                    label = queries[0] if queries else ""
                    print(f"  [tool] google_search ({label})" if label else "  [tool] google_search", flush=True)

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
# Build this function through the first two exercises.
# ─────────────────────────────────────────────────────────────────────────────

def run_digest():
    # TODO 1: create a genai.Client, call interactions.create() with agent=BASE_AGENT,
    # input="Fetch the Hacker News front page and list the top 5 stories.",
    # stream=True, environment="remote", then pass the stream to run_stream()
    # TODO 3: change input= to PROMPT
    # TODO 4: change environment= to a dict with type="remote" and sources=[AGENTS_MD, SKILL_MD, GENERATE_PDF_PY]
    # TODO 5: add set_key(".env", "ENVIRONMENT_ID", environment_id) and set_key(".env", "INTERACTION_ID", interaction_id)
    pass


if __name__ == "__main__":
    run_digest()
