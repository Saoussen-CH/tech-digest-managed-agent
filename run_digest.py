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


def load_source(relative_path: str) -> str:
    """Read a config file from the .agents/ directory."""
    return (BASE_DIR / relative_path).read_text(encoding="utf-8")


# TODO 2: load AGENTS_MD, SKILL_MD, and GENERATE_PDF_PY using load_source()


def run_stream(stream) -> tuple[str, str]:
    """Process a stream of events, printing progress.

    Returns (environment_id, interaction_id) from the completed event.
    """
    import json as _json

    environment_id = None
    interaction_id = None
    pending_tool = None  # function_call name waiting for arguments_delta

    for event in stream:
        event_type = getattr(event, "event_type", None)

        if event_type == "interaction.created":
            print("[agent started]", flush=True)

        elif event_type == "step.start":
            if pending_tool:
                print(flush=True)
                pending_tool = None

            step = getattr(event, "step", None)
            if step:
                stype = getattr(step, "type", "")
                args  = getattr(step, "arguments", None)

                if stype == "function_call":
                    name = getattr(step, "name", "")
                    if name:
                        print(f"  [tool] {name}", end="", flush=True)
                        pending_tool = name

                elif stype == "url_context_call":
                    print("  [tool] url_context", end="", flush=True)
                    pending_tool = "url_context"

                elif stype == "code_execution_call":
                    print("  [tool] run_code", flush=True)

                elif stype == "google_search_call":
                    print("  [tool] google_search", end="", flush=True)
                    pending_tool = "google_search"

        elif event_type == "step.delta":
            delta = getattr(event, "delta", None)
            if delta:
                dtype = getattr(delta, "type", "")
                if dtype == "arguments_delta" and pending_tool:
                    try:
                        args_dict = _json.loads(getattr(delta, "arguments", "") or "{}")
                        if pending_tool == "google_search":
                            queries = args_dict.get("queries", [])
                            label = queries[0] if queries else None
                        elif pending_tool == "url_context":
                            urls = args_dict.get("urls", [])
                            label = urls[0] if urls else None
                        else:
                            label = (args_dict.get("path") or args_dict.get("directory")
                                     or args_dict.get("file_path"))
                        print(f" ({label})" if label else "", flush=True)
                    except Exception:
                        print(flush=True)
                    pending_tool = None
                elif dtype == "text":
                    if pending_tool:
                        print(flush=True)
                        pending_tool = None
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
    # TODO 3: change environment= to a dict with type="remote" and sources=[AGENTS_MD, SKILL_MD, GENERATE_PDF_PY]
    #         and set input="" (AGENTS.md already defines the full workflow)
    pass
    # TODO 4: after print(f"\nDone. environment_id={environment_id}"), add set_key() calls to persist both IDs


if __name__ == "__main__":
    run_digest()
