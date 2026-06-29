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
                        step_dict = vars(step) if hasattr(step, "__dict__") else {}
                        print(f"  [debug] {name} step_keys={list(step_dict.keys())} step={step_dict}", flush=True)
                        path = None
                        if args:
                            args_dict = (args if isinstance(args, dict)
                                         else vars(args) if hasattr(args, "__dict__") else {})
                            for key in ("path", "file_path", "filepath", "directory", "filename", "dir"):
                                path = args_dict.get(key)
                                if path:
                                    break
                            if not path:
                                path = next((v for v in args_dict.values() if isinstance(v, str)), None)
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
            if delta:
                dtype = getattr(delta, "type", "")
                if dtype != "text":
                    print(f"  [debug-delta] type={dtype} delta={vars(delta) if hasattr(delta, '__dict__') else delta}", flush=True)
                elif dtype == "text":
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
    pass
    # TODO 5: after print(f"\nDone. environment_id={environment_id}"), add set_key() calls to persist both IDs


if __name__ == "__main__":
    run_digest()
