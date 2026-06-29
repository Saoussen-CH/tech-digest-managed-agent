---
id: managed-agents-gemini-api
summary: Build a managed agent that fetches live tech news, writes editorial summaries, and generates a PDF, powered by Managed agents on the Gemini API.
status: Draft
authors: Saoussen Chaabnia
categories: AI, Gemini API
tags: web
feedback link: https://github.com/googlecodelabs/feedback/issues/new?title=[managed-agents-gemini-api]
keywords: docType:Codelab, category:AI, product:GeminiAPI

---

# Build a Managed Tech Digest Agent with the Gemini API

## Overview

Duration: 05:00

The AI and tech landscape moves faster than anyone can track. New models, papers, and products drop daily. A digest agent that fetches today's headlines, writes sharp summaries, and generates a PDF every morning would solve that, but building one used to mean picking a framework, defining tools in Python, writing an orchestration loop, packaging a container, and deploying to Cloud Run. All of that before the agent had made a single web request.

Managed agents on the Gemini API changes the equation. You write two markdown config files and a pre-built renderer script, make one API call, and a real Ubuntu sandbox boots, browses the web, writes your summaries, and generates a PDF. No containers. No deployment. No orchestration code.

In this codelab you will build exactly that agent: from an empty function to a working daily digest, one concept at a time.

### What you will build

- Create and run your first managed agent in a real Linux sandbox
- Customize the agent with detailed instructions
- Download the PDF output of the agent
- Continue the conversation to refine the digest without re-fetching the web
- Save the agent config and invoke it by ID in future runs

### What you'll need

- Python 3.10+
- A Gemini API key with billing enabled: [aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)
- ~$1 of API credit (each full run costs $0.30-$1.30)

---

## What is Managed agents on the Gemini API?

Duration: 05:00

### Three levels of AI systems

Before diving into code, here is where Managed Agents fits relative to the two alternatives:

| Level | What It Is | Who Manages Infrastructure? |
|---|---|---|
| **Standard LLM** | You prompt, it replies with text. No hands, no memory, no internet. | N/A: it cannot do anything on its own |
| **Self-Hosted Agent** | You wire up ADK/LangChain/AutoGen + Docker + tools + memory. | You: all of it (or a managed platform like Agent Engine) |
| **Managed Agent** | You give it a goal. Google provisions a secure sandbox. The agent writes code, runs it, reads errors, searches the web, and fixes bugs autonomously. | Google: all of it |

This codelab is about the third row. You supply a task and configuration files. Google handles everything else.

### What you would build with ADK + Cloud Run

To build a news digest agent that browses the web, runs Python, and generates a PDF, you would need all of this with ADK + Cloud Run:

```python
# agent.py: define tools and wire up the agent
from google.adk.agents import LlmAgent
from google.adk.tools import google_search, built_in_code_execution

agent = LlmAgent(
    name="digest-agent",
    model="gemini-2.0-flash",
    instruction=AGENTS_MD,          # your editorial voice and rules
    tools=[google_search, built_in_code_execution],
)
```

```python
# app.py: serve the agent over HTTP
from google.adk.runners import FastApiRunner
runner = FastApiRunner(agent=agent)
app = runner.app
```

```python
# pdf_tool.py: custom tool, install reportlab, render PDF
# scraper.py: custom tool, fetch each news source
# streaming.py: wire agent events to your SSE endpoint
```

```dockerfile
# Dockerfile: package everything
FROM python:3.12
COPY . /app
RUN pip install google-adk reportlab requests
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

```bash
# Deploy to Cloud Run
gcloud run deploy digest-agent \
  --image gcr.io/your-project/digest-agent \
  --set-secrets GEMINI_API_KEY=gemini-key:latest \
  --memory 2Gi
```

That is before the agent has run once. You still own sandbox isolation (so the agent cannot damage your server), package installation, state management between tool calls, and the streaming infrastructure to get events to a client.

### What Managed Agents replaces it with

```python
from google import genai
client = genai.Client()

stream = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input=PROMPT,
    stream=True,
    environment={
        "type": "remote",
        "sources": [          # your config files, mounted at startup
            {
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": AGENTS_MD,
            },
            {
                "type": "inline",
                "target": ".agents/skills/digest-pdf/SKILL.md",
                "content": SKILL_MD,
            },
            {
                "type": "inline",
                "target": ".agents/skills/digest-pdf/scripts/generate_pdf.py",
                "content": GENERATE_PDF_PY,
            },
        ],
    },
)
```

| What ADK + Cloud Run requires | What Managed Agents handles for you |
|---|---|
| Container image + Dockerfile + CI/CD | Fully managed Ubuntu sandbox (Python 3.12, Node 22, 4 CPU / 16 GB RAM) |
| Cloud Run deployment + scaling | Provisioned per interaction, auto-expires after 7 days of inactivity |
| Sandbox isolation | Isolated per interaction |
| Custom PDF tool + `pip install` | Agent installs packages inside the sandbox |
| SSE streaming infrastructure | `stream=True` returns an event iterable |
| Tool definitions in Python | Tools built in: web browse, code execution, file system |
| State management between tool calls | Built into the agent reasoning loop |

You write configuration files (`AGENTS.md`, `SKILL.md`, a pre-built script) and make one API call. Google handles everything else.

### How the sandbox works

```text
interactions.create() call
        │
        ▼
Google provisions Ubuntu sandbox (Python 3.12, Node 22, 4 CPU / 16 GB RAM)
        │
        ▼
Agent reasoning loop:
  plan → fetch URLs → run Python → write files → reason → repeat
        │
        ▼
Events stream back in real time: tool calls, text chunks, completion
        │
        ▼
interaction.completed → environment_id + interaction_id
```

The sandbox persists for 7 days of inactivity. You can resume it with `environment_id` to refine the output, run follow-up tasks, or fork it into a saved named agent.

---

## Set Up

Duration: 05:00

### Option A: Cloud Shell (recommended)

Click the button below to open this codelab in Google Cloud Shell. All dependencies are pre-installed.

[Open in Cloud Shell](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/Saoussen-CH/tech-digest-managed-agent)

### Option B: Local setup

```bash
git clone https://github.com/Saoussen-CH/tech-digest-managed-agent.git
cd tech-digest-managed-agent
```

Install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configure your API key

```bash
cp .env.example .env
cloudshell edit .env
```

Set your key:

```text
GEMINI_API_KEY=your-key-here
```

> aside negative
>
> **Billing required.** The Managed agents on the Gemini API charges for token usage. Each full digest run costs ~$0.30-$1.30. Environment compute (CPU, memory, sandbox execution) is free during the preview period. The free tier does not cover the Interactions API: add prepay credits at [aistudio.google.com/billing](https://aistudio.google.com/billing).

### Install dependencies

```bash
uv sync
```

---

## Make Your First Agent Call

Duration: 10:00

### Open the starter file

```bash
cloudshell edit run_digest.py
```

> aside positive
>
> **Local setup:** open `run_digest.py` in your editor of choice.

`run_digest()` is a stub (just `pass`). Two helpers are already pre-filled above it:

- `load_source(path)`: reads a file from `.agents/` relative to the script. You will use it in the next exercise to mount the editorial voice, PDF playbook, and renderer into the sandbox.
- `run_stream(stream)`: processes the event stream and returns `(environment_id, interaction_id)`. You do not need to write the event loop yourself.

### What to add

**TODO 1:** replace `pass` with:

```python
    from google import genai
    client = genai.Client()

    stream = client.interactions.create(
        agent=BASE_AGENT,
        input="Fetch the Hacker News front page and list the top 5 stories.",
        stream=True,
        environment="remote",
    )

    environment_id, interaction_id = run_stream(stream)
    print(f"\nDone. environment_id={environment_id}")
```

### What each part does

`genai.Client()` reads `GEMINI_API_KEY` from the environment. Everything else goes through this client.

`interactions.create()` is the core call. Four parameters make it work:

- **`agent=BASE_AGENT`**: selects the Antigravity agent (`antigravity-preview-05-2026`), a general-purpose managed agent powered by Gemini 3.5 Flash. It comes with three built-in tools enabled by default: `code_execution` (run Bash, Python, Node.js), `google_search`, and `url_context` (fetch and read web pages). Filesystem tools (`read_file`, `write_file`, `list_files`) are enabled automatically when you pass the `environment` parameter. One call provisions a fully managed Ubuntu environment with Python 3.12, Node.js 22, git, pip, and curl pre-installed. No container to build, no deployment to run.
- **`input`**: the task for this run. The agent browses Hacker News and reasons about the results.
- **`environment="remote"`**: provisions a fresh cloud sandbox for this interaction.
- **`stream=True`**: returns an iterable of events instead of blocking. Without it, the call waits 30-90 seconds and returns all output at once as `interaction.output_text`. With streaming you see the agent reason and act as it happens. Streaming is not an advanced feature here: it is the right default, because a 90-second black box gives you no signal about whether the agent is working or stuck.

**What you just provisioned:** every `interactions.create()` call boots a dedicated sandbox:

| Component | Specification |
|---|---|
| Operating System | Isolated Ubuntu Linux environment |
| Pre-installed Runtimes | Python 3.12, Node.js 22, Bash |
| Compute | 4 CPU cores, 16 GB RAM |
| Context Management | Auto-compaction triggers at ~135k tokens |
| Networking | Outbound web access via Egress Proxy |

The agent can install any package with `pip` or `npm`, read and write files, and make outbound web requests. Your machine and credentials are never touched.

**`environment_id`** is a handle to the sandbox that just ran. After `interaction.completed`, the sandbox does not shut down: it stays alive for up to 7 days. The `environment_id` is how you get back to it. Pass it to a second `interactions.create()` call and the agent resumes on the same filesystem, with the same files and installed packages, as if it never left. The next step uses it to download the PDF without re-running the agent, and the step after that uses it to continue the conversation.

**`interaction_id`** is a handle to the conversation turn that just completed. Pass it as `previous_interaction_id` in the next call and the agent has full memory of what it said and did in this turn.

### Verify

```bash
uv run python run_digest.py
```

You should see live output as the agent works:

```text
[agent started]
  [tool] run_code
Here are the top 5 stories currently on the Hacker News front page:
...
Done. environment_id=863e7fa217a54236e278eb61b2e2538c
```

The API returns a real `environment_id` even with `environment="remote"`. The sandbox ran. What is missing is config: no voice, no skill, no PDF generator. The agent just printed stories as text and stopped. The next step adds those.

Each line of output maps to an event from `run_stream()`:

| `step.type` | What it is | What `run_stream()` prints |
|---|---|---|
| `"url_context_call"` | agent fetching a URL | `[tool] url_context (https://...)` |
| `"code_execution_call"` | agent running code in the sandbox | `[tool] run_code` |
| `"google_search_call"` | agent searching the web | `[tool] google_search (query...)` |
| `"function_call"` | file tools and others | `[tool] read_file (/workspace/...)` |
| `step.delta` where `delta.type == "text"` | agent writing text | streamed directly to stdout |

---

## Customize the Agent

Duration: 08:00

The agent had no instructions: no voice, no skill, no PDF generator. In this step you load the configuration files from `.agents/` and mount them into the sandbox.

> aside positive
>
> **This is the fastest way to build a custom agent.** You are customizing the Antigravity agent for this run without registering anything. The next step shows how to bake this configuration permanently into a named agent so you never pass sources again.

### What to change

Make four changes to `run_digest.py`:

**TODO 1:** Below `load_source()`, add the three module-level constants (these sit outside `run_digest()`, at the top of the file):

```python
AGENTS_MD       = load_source(".agents/AGENTS.md")
SKILL_MD        = load_source(".agents/skills/digest-pdf/SKILL.md")
GENERATE_PDF_PY = load_source(".agents/skills/digest-pdf/scripts/generate_pdf.py")
```

Open each file to see what you are loading: `AGENTS.md` sets the editorial voice and workflow rules; `SKILL.md` is the step-by-step PDF playbook; `generate_pdf.py` is the pre-built renderer the agent will run.

> aside positive
>
> **Why `AGENTS.md` instead of `system_instruction`?** The Interactions API also accepts a `system_instruction` string parameter directly. Both approaches work and are additive when used together. `AGENTS.md` is the better fit here because it lives alongside your code in the repo, is version-controlled with the rest of the project, and is always in the agent's context from the first token. Use `system_instruction` for quick per-call tweaks; use `AGENTS.md` for long-form persona definitions and guidelines you want to version alongside your agent.

> aside positive
>
> **Why `PROMPT`?** `AGENTS.md` and `SKILL.md` tell the agent HOW to generate a digest, but the agent still needs a trigger to know WHEN to start and WHERE to save the file. `PROMPT` provides that: it activates the skill and specifies the output path. Without it the agent has no task to begin.

Now make three changes inside `run_digest()`:

2. Change `input` to `PROMPT`

3. Change `environment` from `"remote"` to:

```python
        environment={
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": AGENTS_MD,
                },
                {
                    "type": "inline",
                    "target": ".agents/skills/digest-pdf/SKILL.md",
                    "content": SKILL_MD,
                },
                {
                    "type": "inline",
                    "target": ".agents/skills/digest-pdf/scripts/generate_pdf.py",
                    "content": GENERATE_PDF_PY,
                },
            ],
        },
```

4. Add these lines right after `print(f"\nDone. environment_id={environment_id}")`:

```python
    set_key(".env", "ENVIRONMENT_ID", environment_id)
    set_key(".env", "INTERACTION_ID", interaction_id)
```

(`set_key` is already imported at the top of `run_digest.py`.)

This writes both IDs to `.env` during this run, so the next step can download the PDF without re-running the agent.

### What each source does

Each source is a file mounted into the sandbox filesystem at startup before the agent runs. The `target` paths match where the Antigravity harness expects to find them:

```
.agents/
├── AGENTS.md                              ← auto-loaded as global instructions
└── skills/
    └── digest-pdf/
        ├── SKILL.md                       ← auto-discovered and registered as a skill
        └── scripts/
            └── generate_pdf.py            ← pre-built renderer the agent can run
```

| `target` path | Variable | What the harness does with it |
|---|---|---|
| `.agents/AGENTS.md` | `AGENTS_MD` | Auto-loaded as persistent instructions: editorial voice, workflow, execution rules |
| `.agents/skills/digest-pdf/SKILL.md` | `SKILL_MD` | Auto-discovered and registered as a named skill; the agent invokes it by name |
| `.agents/skills/digest-pdf/scripts/generate_pdf.py` | `GENERATE_PDF_PY` | Pre-built PDF renderer; the agent writes `summaries.json` then runs this script |

> aside positive
>
> **Skills are a cross-platform standard** (agentskills.io). They give the agent procedural memory: not just what to know, but how to do a specific task step by step. The body of `SKILL.md` loads only when the skill triggers; metadata (name + description) stays in context all along. This is called progressive disclosure, and it keeps the context window clean.
>
> Two things to notice here:
>
> - **Skill vs AGENTS.md**: `AGENTS.md` is always in the agent's context from the first token: voice, workflow rules, execution constraints. `SKILL.md` loads on demand only when the agent decides the skill is needed for the task. `AGENTS.md` should stay tight; the recommended pattern is to include a short catalog at the bottom that lists available skills so the agent knows what to look for. The `## Skills` table in `.agents/AGENTS.md` is exactly that: it tells the agent that `digest-pdf` exists, so the harness can load its full `SKILL.md` when the task calls for it.
> - **Managed Agents vs ADK**: ADK uses the programmatic route: `load_skill_from_dir("skills/digest-pdf")` then `SkillToolset(skills=[skill])` in Python code. With Managed Agents you use the inline route: mount the file via `environment.sources` and the harness discovers it from `.agents/skills/*/SKILL.md` automatically. No registration code.

### Verify

```bash
uv run python run_digest.py
```

The run now takes 1-3 minutes. You should see the agent reading config files, writing summaries, and saving the PDF:

```text
[agent started]
  [tool] run_code
  [tool] run_code
  [tool] read_file (/workspace/summaries.json)
  [tool] run_code
I have successfully created today's tech news digest.
...editorial summaries in the configured voice...
Done. environment_id=8d30ba94-f2c8-49bd-bbd4-e4a130e28e2d
```

`environment_id` is now a real value: the sandbox ran with your config files and the agent created `digest.pdf`. The next step downloads it.

---

## Download the PDF

Duration: 05:00

The agent wrote `digest.pdf` to `/workspace/digest.pdf` inside the sandbox. The environment snapshot is available as a tar archive via the Gemini Files API.

> aside positive
>
> **In a real project**, the download would live inside `run_digest()` right after the event loop (same run, same `environment_id`, no separate file). In this codelab it lives in `download_pdf.py` so you can re-download without re-running the agent. The `set_key` lines you added in the previous step write both IDs to `.env` automatically, so this file can read them straight away.

Install `requests` if needed:

```bash
uv pip install requests
```

### What to fill in

Open `download_pdf.py`. It has two TODOs.

**TODO 1:** fill in the `requests.get()` call:

```python
r = requests.get(
    f"https://generativelanguage.googleapis.com/v1beta/files/environment-{environment_id}:download",
    params={"alt": "media"},
    headers={"x-goog-api-key": api_key},
    allow_redirects=True,
)
r.raise_for_status()
```

The URL addresses the sandbox snapshot. `params={"alt": "media"}` returns raw bytes instead of metadata. Your existing `GEMINI_API_KEY` authenticates the Files API too.

**TODO 2:** extract only the PDF from the tar archive and read its bytes:

```python
            tar.extract("workspace/digest.pdf", path=tmp)
```

The agent saved the PDF to `/workspace/digest.pdf` inside the sandbox, so that is its path in the tar. Extracting only this one member (rather than calling `extractall()`) avoids permission errors on Mac caused by `/dev` entries in the snapshot.

### Verify

```bash
uv run python download_pdf.py
```

```text
Saved digest.pdf (48,231 bytes)
```

Open `digest.pdf` in the same directory. It contains the formatted digest the agent generated from live web pages.

---

## Continue the Conversation

Duration: 05:00

You already have `digest.pdf`. If you just wanted the file, you are done. This step is about something different: asking the agent to **change** the digest without re-fetching the web.

The sandbox is still alive. The agent still has `/workspace/digest.pdf` and remembers every story it summarized. A second `interactions.create()` call sends a follow-up message into that same sandbox. Here you ask it to add a "Why it matters" note under each story, and it updates the PDF in place, with no re-fetching and no re-summarizing.

### What to fill in

Open `refine_digest.py`. It has three TODOs.

**TODOs 1 and 2:** fill in the two multi-turn parameters inside `interactions.create()`:

```python
    environment=environment_id,
    previous_interaction_id=interaction_id,
```

`environment=environment_id` resumes the same sandbox with its files and packages. `previous_interaction_id=interaction_id` gives the agent its conversation history. Nothing else changes from the first call.

**TODO 3:** persist the new `interaction_id` back to `.env` after the event loop:

```python
set_key(".env", "INTERACTION_ID", interaction_id)
```

Every `interactions.create()` call produces a new `interaction_id`. Writing it back means the next run passes this refinement as `previous_interaction_id`, chaining turns correctly. The sandbox ID never changes so `ENVIRONMENT_ID` does not need to be updated.

### The two parameters that make multi-turn work

| ID | What it preserves | Analogy |
|---|---|---|
| `environment=environment_id` | Files, installed packages, system state: everything on the Linux filesystem | Keeping the same office desk between meetings |
| `previous_interaction_id=interaction_id` | Conversation history: what the agent said and did in prior turns | Remembering what was discussed in the last meeting |

You can pass either ID independently:

- `environment_id` only: reuse files and packages, but start a fresh conversation. Useful for a new task in the same workspace.
- `previous_interaction_id` only: continue the conversation context, but in a fresh sandbox (files are gone).
- Both: full continuity, which is what this step uses.

Without `environment_id`: blank sandbox, no PDF.
Without `previous_interaction_id`: no context, agent cannot refine a specific section.

> aside positive
>
> **This replaces the session management you would write with ADK + Cloud Run.** With ADK you store conversation history in a database and inject it into each request. With Managed Agents you pass two IDs and the platform handles the rest.

### Verify

```bash
uv run python refine_digest.py
```

The stream should be quick; the agent is not re-fetching anything. After it finishes:

```text
Refinement done.
Saved digest_v2.pdf (52,418 bytes)
```

Open `digest_v2.pdf` and compare it to `digest.pdf`. Each story should now have a "Why it matters" line added.

---

## Persist a Managed Agent Config

Duration: 05:00

Every call so far has passed `AGENTS.md`, `SKILL.md`, and `generate_pdf.py` inline. That works, but your calling code carries the full file contents on every run. `agents.create()` bakes the configuration into a saved named agent on Google's side. The next invocation just passes the agent ID:

```
Inline calls:   send sources on every call
Named agent:    bake once → invoke by ID, no sources
```

### What to fill in

Open `save_agent.py`. It has one TODO (TODO 1).

> aside negative
>
> `AGENTS_MD`, `SKILL_MD`, and `GENERATE_PDF_PY` are imported from `run_digest.py`. Make sure you completed the Customize step and added those three loading lines before running this file.

Notice that the constants are imported directly from `run_digest.py` (no duplication):

```python
from run_digest import BASE_AGENT, AGENTS_MD, SKILL_MD, GENERATE_PDF_PY
```

**TODO 1:** fill in the `agents.create()` call:

```python
agent = client.agents.create(
    id="my-digest",
    base_agent=BASE_AGENT,
    description="Daily tech digest with editorial voice and PDF generation.",
    base_environment={
        "type": "remote",
        "sources": [
            {
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": AGENTS_MD,
            },
            {
                "type": "inline",
                "target": ".agents/skills/digest-pdf/SKILL.md",
                "content": SKILL_MD,
            },
            {
                "type": "inline",
                "target": ".agents/skills/digest-pdf/scripts/generate_pdf.py",
                "content": GENERATE_PDF_PY,
            },
        ],
    },
)
```

`base_environment` (not `environment`) is the key difference from the inline call in the previous step: the sources are stored on Google's side and mounted automatically on every future invocation. Run it once, not on every digest run.

### Verify: save the agent

```bash
uv run python save_agent.py
```

```text
Saved: my-digest
my-digest: Daily tech digest with editorial voice and PDF generation.
```

> aside negative
>
> **409 Conflict?** An agent named `my-digest` already exists from a previous run. The starter file deletes it automatically before creating a new one, so re-running is safe.

### Invoke the saved agent

Open `invoke_agent.py`. It calls the saved agent by ID with no sources:

```python
stream = client.interactions.create(
    agent="my-digest",
    input=PROMPT,
    stream=True,
    environment="remote",
)
```

Compare this to the inline call: `agent=BASE_AGENT` is replaced by `"my-digest"`, and the full `environment` block with three inline sources is replaced by `environment="remote"`. The config is already baked in on Google's side.

### Verify: invoke the saved agent

```bash
uv run python invoke_agent.py
```

You should see the same live stream as the inline run, but the call carries no source files. After the run, `ENVIRONMENT_ID` and `INTERACTION_ID` in `.env` are updated so you can continue with `refine_digest.py` as before.

```text
[agent started]
  [tool] read_file
  [tool] write_file
  [tool] run_code
I have successfully created today's tech news digest.
Done. environment_id=9a1c3e02-...
```

---

## Clean Up

Duration: 02:00

The sandbox auto-expires after 7 days of inactivity. No servers to stop. No containers to delete.

If you saved an agent config, delete it:

```bash
uv run python delete_agent.py
```

---

## Summary

Duration: 02:00

You built a managed agent from scratch, one concept at a time. Here is what each exercise taught:

| Exercise | Concept | Key API |
|---|---|---|
| Make your first call | Provision a real Linux sandbox and stream its events live | `interactions.create(agent, input, environment, stream=True)`, `event.event_type` |
| Customize the agent | Mount config files; persist IDs to `.env` in the same run | `environment.sources`, `set_key` |
| Download the PDF | Download the PDF without re-running the agent | Gemini Files API `:download` in `download_pdf.py` |
| Continue the conversation | Continue the conversation without re-fetching the web | `environment=environment_id`, `previous_interaction_id=interaction_id` |
| Persist agent config | Persist agent config; invoke by ID, no sources needed | `agents.create()`, `agents.list()` |

### Key patterns

1. **One call, one sandbox**: `interactions.create()` handles all infrastructure (no containers to deploy, no packages to install locally)
2. **Progressive streaming**: `stream=True` turns a 90-second black box into a live feed of tool calls and text chunks
3. **Inline sources**: mount `AGENTS.md`, `SKILL.md`, and pre-built scripts into the sandbox without any upload or deployment step
4. **Harness auto-discovery**: files placed in `.agents/` are picked up automatically (no SDK config required)
5. **Two-dimensional state**: `environment_id` tracks files and packages; `previous_interaction_id` tracks conversation context; either can be passed independently
6. **Snapshot download**: the environment is a full filesystem tar, accessible via the Gemini Files API
7. **Named agents**: `agents.create()` bakes config permanently; future calls pass only the agent ID and `environment="remote"`, with no sources

### ADK + Cloud Run vs. Managed Agents: the difference at a glance

| Capability | ADK + Cloud Run | Managed agents on the Gemini API |
|---|---|---|
| Provision a sandbox | `docker build` + `gcloud run deploy` | `interactions.create()` |
| Define tools | Python functions registered with the agent | Built in: web browse, code execution, file system |
| Install packages | `pip install` in Dockerfile | Agent runs `pip install` inside sandbox |
| Stream events | Custom SSE infrastructure | `stream=True` |
| Continue a session | Session database + context injection | `environment_id` + `previous_interaction_id` |
| Config files | Hard-coded in agent or injected at startup | Mounted via `environment.sources` |
| Infrastructure to manage | Container, Cloud Run, IAM, secrets | None |

### Next steps

- Read the [Managed agents on the Gemini API documentation](https://ai.google.dev/gemini-api/docs/managed-agents-quickstart)

