# Build a Managed Tech Digest Agent with the Gemini API

Codelab starter repo. Follow the codelab to build a managed agent that fetches live tech news, writes editorial summaries, and generates a PDF, powered by [Managed agents on the Gemini API](https://ai.google.dev/gemini-api/docs/managed-agents).

**Codelab:** [https://codelabs.developers.google.com/tech-digest-managed-agent](https://codelabs.developers.google.com/tech-digest-managed-agent)

## What you build

An agent that runs in a Google-hosted Linux sandbox and:

1. Fetches today's headlines from Hacker News, TechCrunch, and The Verge
2. Writes sharp editorial summaries in a configured voice
3. Generates a formatted PDF and saves it to `/workspace/digest.pdf`

## Repo layout

```
run_digest.py        # Step 1 & 2: first agent call, then customize with voice + skill
download_pdf.py      # Step 3: download digest.pdf from the sandbox
refine_digest.py     # Step 4: multi-turn: ask the agent to refine the digest
save_agent.py        # Step 5: save your configured agent by ID
invoke_agent.py      # Step 5: invoke the saved agent
delete_agent.py      # cleanup helper
.agents/
  AGENTS.md          # editorial voice loaded into every run
  skills/digest-pdf/
    SKILL.md         # PDF generation playbook
    scripts/generate_pdf.py
codelab/
  index.lab.md       # codelab source (claat markdown)
  generate.sh        # regenerate docs/ from index.lab.md
docs/                # generated HTML served by GitHub Pages
pyproject.toml
```

## Setup

```bash
# 1. Clone
git clone https://github.com/Saoussen-CH/tech-digest-managed-agent
cd tech-digest-managed-agent

# 2. Install dependencies (requires uv)
uv sync

# 3. Set your API key
cp .env.example .env
cloudshell edit .env   # or open .env in your editor
```

Get a Gemini API key at [aistudio.google.com](https://aistudio.google.com).

## Run

Follow the codelab steps in order. Each file has numbered TODOs to fill in.
