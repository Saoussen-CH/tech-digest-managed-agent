from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()
try:
    client.agents.delete(id="my-digest")
    print("Deleted: my-digest")
except Exception as e:
    print(f"Nothing to delete: {e}")
