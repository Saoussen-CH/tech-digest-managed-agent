import os
import requests
import tarfile
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def fetch_pdf(environment_id: str) -> bytes:
    """Download digest.pdf from the sandbox environment snapshot."""
    api_key = os.environ["GEMINI_API_KEY"]

    # TODO 1: Download the environment snapshot from the Gemini Files API.
    # Use requests.get() with params={"alt": "media"} and headers={"x-goog-api-key": api_key}.
    # Call r.raise_for_status() after.
    raise NotImplementedError("Fill in TODO 1 before running this file.")

    with tempfile.TemporaryDirectory() as tmp:
        tar_path = Path(tmp) / "snapshot.tar"
        tar_path.write_bytes(r.content)
        with tarfile.open(tar_path) as tar:
            # TODO 2: Read the PDF bytes from the extracted sandbox filesystem.
            # The agent saved the file to /workspace/digest.pdf inside the sandbox.
            # Find the member by suffix (the tar path prefix varies) and extract it.
            raise NotImplementedError("Fill in TODO 2 before running this file.")
        return next(Path(tmp).rglob("digest.pdf")).read_bytes()


if __name__ == "__main__":
    environment_id = os.environ["ENVIRONMENT_ID"]
    pdf_bytes = fetch_pdf(environment_id)
    Path("digest.pdf").write_bytes(pdf_bytes)
    print(f"Saved digest.pdf ({len(pdf_bytes):,} bytes)")
