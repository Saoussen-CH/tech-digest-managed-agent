import os
from pathlib import Path
from dotenv import load_dotenv, set_key
from google import genai
from run_digest import BASE_AGENT, run_stream
from download_pdf import fetch_pdf

load_dotenv()

environment_id = os.environ["ENVIRONMENT_ID"]
interaction_id  = os.environ["INTERACTION_ID"]

client = genai.Client()

print("Refining digest...", flush=True)

stream = client.interactions.create(
    agent=BASE_AGENT,
    input="Add a one-line 'Why it matters' note under each story.",
    # TODO 1: pass environment=environment_id to resume the same sandbox
    # TODO 2: pass previous_interaction_id=interaction_id to continue the conversation
    stream=True,
)

_, interaction_id = run_stream(stream)

# TODO 3: persist the updated interaction_id back to .env using set_key
print("\nRefinement done.")

pdf_bytes = fetch_pdf(environment_id)
Path("digest_v2.pdf").write_bytes(pdf_bytes)
print(f"Saved digest_v2.pdf ({len(pdf_bytes):,} bytes)")
