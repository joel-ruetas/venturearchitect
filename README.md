# 🚀 VentureArchitect – Business Plan Copilot

VentureArchitect is a **multi-agent business plan generator** built on top of the [Google AI Agents Development Kit (ADK)](https://github.com/google-deepmind/ai-agents). You give it a short description of a business idea (e.g. *“I want to create a garage sale app”*), and it orchestrates several specialist agents to produce a **long, structured, professional business plan**.

You can use VentureArchitect in three ways:

1.  **CLI mode** – interactive terminal app.
2.  **Web UI** – simple FastAPI web app.
3.  **Evaluation mode** – run automated quality checks with `adk eval`.

-----

## 1\. Project Features

  * **Multi-agent architecture**

      * `discovery_agent` – infers a structured business profile from your idea.
      * `research_agent` – enriches with market & competitive context.
      * `strategy_agent` – builds positioning, GTM, and roadmap.
      * `financial_agent` – drafts simple projections and monetization models.
      * `narrative_agent` – assembles a polished, long-form business plan.
      * `evaluation_agent` – (optional) grades the plan for clarity & completeness.

  * **Professional output**

      * Sections like *Executive Summary, Problem, Solution, Market, Competition, Business Model, Go-to-Market, Financials, Risks, Roadmap*, etc.
      * Formal tone suitable for internal docs, pitch prep, or first-pass investor decks.

  * **Web UI**

      * Minimal single-page app built with FastAPI + Jinja templates.
      * Lets you paste your idea, generate, and copy the plan quickly.

  * **Automated evaluation (optional)**

      * Uses ADK’s evaluation tooling to replay saved test cases from `eval/`.
      * Helps guard against regressions as you tweak prompts or code.

-----

## 2\. Directory Structure

At a high level the project looks like this:

```text
VENTUREARCHITECT/
├─ .venv/                 # Local virtual environment (not committed)
├─ business_plan_agent/   # Thin adapter package for ADK eval CLI
│  ├─ __init__.py
│  └─ agent.py            # Exposes root_agent for evaluation
│
├─ eval/
│  ├─ business_plan.evalset.json  # Example evaluation cases
│  └─ test_config.json            # Evaluation thresholds / criteria
│
├─ venturearchitect/
│  ├─ __init__.py
│  ├─ .agent_engine_config.json   # ADK engine config (if using a2a_server)
│  ├─ web_app.py                  # FastAPI web UI
│  ├─ runner_app.py               # CLI entrypoint
│  ├─ tools.py                    # Shared helper tools (if any)
│  └─ agents/
│     ├─ __init__.py
│     ├─ config.py                 # Model + shared configuration
│     ├─ discovery_agent.py
│     ├─ research_agent.py
│     ├─ strategy_agent.py
│     ├─ financial_agent.py
│     ├─ narrative_agent.py
│     ├─ evaluation_agent.py
│     └─ root_agent.py             # Orchestrator that calls all sub-agents
│
├─ requirements.txt
└─ README.md
```

> You may also have extra files (e.g., `.env`, `.gitignore`, `.adk/`) depending on how you created the project.

-----

## 3\. Prerequisites

  * **Python:** **3.10+** (project tested with 3.11).
  * **Git** installed.
  * A **Gemini API key** from Google AI Studio.

-----

## 4\. Getting Started

### 4.1. Clone the repository

Replace the placeholder URL with the actual URL of your repo (GitHub, GitLab, etc.):

```bash
git clone https://github.com/joel-ruetas/venturearchitect.git
cd venturearchitect
```

### 4.2. Create & activate a virtual environment

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate
```

You should see `(.venv)` in your shell prompt.

### 4.3. Install dependencies

```bash
pip install -r requirements.txt
```

If you plan to use evaluation features, also install:

```bash
pip install "google-adk[eval]"
```

### 4.4. Configure your Gemini API key

Create a **`.env`** file in the project root (same folder as `README.md`):

```env
GOOGLE_API_KEY=your_api_key_here
```

> You can generate an API key from Google AI Studio. The app uses `GOOGLE_API_KEY` via `dotenv` (`load_dotenv()`).

-----

## 5\. Running the CLI App

The CLI app is the quickest way to try VentureArchitect.

From the project root, with your `venv` activated:

```bash
python -m venturearchitect.runner_app
```

You should see something like:

```text
VentureArchitect – Business Plan Copilot
Describe your business idea in 2–5 sentences.

Enter a brief description of your business idea:
> I want to create a garage sale app
```

The app will:

1.  Build an internal business profile from your sentence.
2.  Call the internal research/strategy/financial/narrative agents.
3.  Print a multi-section business plan back to the console.

-----

## 6\. Running the Web UI

The project also includes a minimal web UI for easier use.

### 6.1. Start the server

From the project root:

```bash
uvicorn venturearchitect.web_app:app --reload
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 6.2. Use the UI

1.  Open your browser and go to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**
2.  Enter your business idea into the text area (e.g. “I want to create a garage sale app”).
3.  Click **Generate Plan**.
4.  Wait for the result section to fill with the generated business plan.
5.  Copy it into your document editor of choice (Notion, Google Docs, Word, etc.).

> **If you see a 500 error:**
>
>   * Check that `GOOGLE_API_KEY` is correctly set in `.env`.
>   * Look at the Uvicorn console output for the stack trace.

-----

## 7\. How the Multi-Agent System Works

At a high level:

| Agent | Role | Details |
| :--- | :--- | :--- |
| **Root Agent** (`root_agent.py`) | Orchestrator | Receives the user’s raw idea. Calls sub-agents in sequence (or via tool-like function calls). Aggregates their outputs into a final long-form plan. |
| **Sub-Agents** (`agents/*.py`) | Specialists | |
| `discovery_agent.py` | Profile Extractor | Extracts a structured profile: business name, one-liner, problem & solution outline, target customer, geography, constraints, etc. |
| `research_agent.py` | Context Provider | Expands on: market context, competitor types, relevant macro trends. (Uses the underlying model; you can bias it toward your own assumptions with detailed instructions.) |
| `strategy_agent.py` | Strategist | Converts the profile + research into: positioning & differentiation, go-to-market strategy, product roadmap & milestones. |
| `financial_agent.py` | Financial Modeler | Produces: simple revenue model, 2–3 year projections with high-level assumptions, commentary on break-even & unit economics. |
| `narrative_agent.py` | Report Assembler | Assembles everything into a polished, cohesive business plan with sections, headings, and professional tone. |
| `evaluation_agent.py` (optional) | Quality Checker | Can be used to generate quality feedback or scoring on plans (e.g. clarity, completeness, risks). |
| **Configuration** (`config.py`) | Model Tuner | Central place for: model name (`gemini-2.5-flash-lite`, etc.), retry settings, temperature / max tokens, shared system prompts. Changing defaults here lets you tune behavior without touching the agents. |

-----

## 8\. Evaluation with `adk eval` (Optional / Advanced)

The project includes an evaluation harness so you can regression-test plan quality.

### 8.1. Files involved

  * `business_plan_agent/agent.py`: Exposes a `root_agent` object in the shape that ADK’s eval tooling expects.
  * `eval/business_plan.evalset.json`: Defines concrete test cases. Example: “simple SaaS tool for freelance designers”, “local dog-walking and pet-sitting service in Toronto”.
  * `eval/test_config.json`: Defines evaluation criteria (e.g. minimum `response_match_score`).

### 8.2. Run the evaluation

From the project root:

```bash
adk eval business_plan_agent eval/business_plan.evalset.json \
  --config_file_path=eval/test_config.json \
  --print_detailed_results
```

**What this does:**

1.  Spins up the `business_plan_agent.root_agent`.
2.  Replays each conversation in `business_plan.evalset.json`.
3.  Compares the current responses and “tool trajectory” (agent calls) with the expected data.
4.  Prints a summary and detailed diagnostics if a case fails.

> **Note:** ADK evaluation features are marked **EXPERIMENTAL** and may log warnings or “unclosed client session” messages when the process exits. For CLI-style runs, these are noisy but generally harmless.

-----

## 9\. Customization & Extension

Some quick ways to adapt VentureArchitect to your needs:

  * **Adjust tone and style:** Edit the instructions in `narrative_agent.py` (e.g., make it more investor-oriented, shorter, or more academic).
  * **Change level of detail:**
      * For shorter plans, instruct the narrative agent to limit each section.
      * For more depth, increase section count or ask it to include appendices.
  * **Add domain-specific sections:** For example, for healthcare or fintech:
      * Add a “Regulatory & Compliance” section.
      * Introduce new sub-agents that focus on regulations or clinical evidence.
  * **Swap or tune the model:** In `config.py`, change the model name (e.g. to a higher-capacity Gemini model) or modify temperature / max output tokens.

> Whenever you change agent behavior significantly, you can:
>
>   * Update or add eval cases in `eval/business_plan.evalset.json`.
>   * Re-run `adk eval` to see whether you’ve improved or regressed on your defined scenarios.

-----

## 10\. Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **“No GOOGLE\_API\_KEY set” / model errors** | Ensure `.env` exists and includes a valid key. Make sure the virtual environment can see it (`python-dotenv` is used in `runner_app.py` / `web_app.py`). |
| **`adk eval` can’t find the agent** | Confirm directory structure: `business_plan_agent/` contains `__init__.py` and `agent.py` (which defines: `root_agent = venture_architect_root_agent`). Make sure `business_plan_agent` is on `PYTHONPATH` (from repo root, it is). |
| **Uvicorn 500 errors** | Check the console stack trace. Common causes: Missing API key, Mis-typed environment variables, Network issues reaching Gemini API. |

-----

## 11\. License & Credits

This project my Capstone Project for the Kaggle 5-Day Agents Intensive Course patterns and uses the Google ADK for multi-agent orchestration and evaluation.

> See the [LICENSE](./LICENSE) file for details.