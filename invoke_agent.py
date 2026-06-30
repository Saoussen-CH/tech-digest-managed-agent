"""
Invoke the saved 'my-digest' agent by ID.
Run this after save_agent.py to confirm the saved config works.
"""
from dotenv import load_dotenv, set_key
from google import genai
from run_digest import run_stream

load_dotenv()

client = genai.Client()

print("Invoking saved agent my-digest...", flush=True)

stream = client.interactions.create(
    agent="my-digest",
    input="",
    stream=True,
    environment="remote",
)

environment_id, interaction_id = run_stream(stream)
print(f"\nDone. environment_id={environment_id}")
set_key(".env", "ENVIRONMENT_ID", environment_id)
set_key(".env", "INTERACTION_ID", interaction_id)
