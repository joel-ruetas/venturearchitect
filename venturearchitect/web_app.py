# venturearchitect/web_app.py

import os
import uuid
from textwrap import dedent

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types

from venturearchitect.agents.root_agent import venture_architect_root_agent

# ------------------------------------------------------------
# Environment / App Init
# ------------------------------------------------------------

load_dotenv()

app = FastAPI(
    title="VentureArchitect – Business Plan Copilot",
    description="Web UI for generating professional business plans.",
)

# Shared session service + runner (IMPORTANT: one instance)
session_service = InMemorySessionService()

runner = Runner(
    agent=venture_architect_root_agent,
    app_name="agents",  # must match when creating sessions
    session_service=session_service,
    plugins=[LoggingPlugin()],
)

# ------------------------------------------------------------
# Request / Response Models
# ------------------------------------------------------------

class GenerateRequest(BaseModel):
    idea: str


# ------------------------------------------------------------
# HTML UI
# ------------------------------------------------------------

HTML_PAGE = dedent(
    """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>VentureArchitect – Business Plan Copilot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { background: #0f172a; }
            textarea::-webkit-scrollbar,
            pre::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            textarea::-webkit-scrollbar-thumb,
            pre::-webkit-scrollbar-thumb {
                background: #64748b;
                border-radius: 9999px;
            }
        </style>
    </head>
    <body class="min-h-screen text-slate-100">
        <div class="max-w-6xl mx-auto px-4 py-6">
            <!-- Header -->
            <header class="mb-6 flex items-center justify-between gap-4">
                <div>
                    <h1 class="text-2xl md:text-3xl font-semibold flex items-center gap-2">
                        <span class="inline-flex items-center justify-center w-9 h-9 rounded-xl bg-sky-500/20 text-sky-400 border border-sky-500/40">
                            🧠
                        </span>
                        <span>VentureArchitect – Business Plan Copilot</span>
                    </h1>
                    <p class="text-slate-400 mt-1 text-sm md:text-base">
                        Describe your business idea and generate a structured, professional business plan.
                    </p>
                </div>
                <div class="hidden md:flex items-center gap-3 text-xs text-slate-400">
                    <div class="px-3 py-1 rounded-full border border-slate-700 bg-slate-900/60">
                        Powered by <span class="text-sky-400 font-semibold">Gemini + ADK</span>
                    </div>
                </div>
            </header>

            <!-- Main Layout -->
            <main class="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
                <!-- Left: Idea Input -->
                <section class="bg-slate-900/60 border border-slate-700/60 rounded-2xl p-4 md:p-5 shadow-lg shadow-black/40">
                    <h2 class="text-lg font-semibold mb-2 flex items-center gap-2">
                        <span class="text-sky-400">📝</span>
                        Your Business Idea
                    </h2>
                    <p class="text-xs md:text-sm text-slate-400 mb-3">
                        Enter 2–5 sentences describing your business. The copilot will write a long, formal,
                        investor-ready business plan for you.
                    </p>

                    <textarea
                        id="idea"
                        class="w-full h-44 md:h-56 resize-y rounded-xl bg-slate-950/70 border border-slate-700/70 px-3 py-2 text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-sky-500/70 focus:border-sky-500 placeholder:text-slate-500"
                        placeholder="Example: I want to build a cross-platform garage sale app that lets neighbours list weekend sales, browse items on a map, and drive more foot traffic through personalized recommendations and local promotion tools."
                    ></textarea>

                    <div class="mt-4 flex items-center justify-between gap-3">
                        <small id="status" class="text-xs text-slate-500"></small>
                        <button
                            id="generateBtn"
                            class="inline-flex items-center gap-2 rounded-full bg-sky-500 hover:bg-sky-400 text-slate-950 font-medium text-sm md:text-base px-4 py-2 shadow-lg shadow-sky-500/30 disabled:opacity-60 disabled:cursor-not-allowed disabled:shadow-none transition"
                        >
                            <span id="btnIcon">⚡</span>
                            <span>Generate Plan</span>
                        </button>
                    </div>
                </section>

                <!-- Right: Output -->
                <section class="bg-slate-900/60 border border-slate-700/60 rounded-2xl p-4 md:p-5 shadow-lg shadow-black/40 flex flex-col min-h-[260px]">
                    <div class="flex items-center justify-between gap-2 mb-2">
                        <h2 class="text-lg font-semibold flex items-center gap-2">
                            <span class="text-emerald-400">📄</span>
                            Generated Business Plan
                        </h2>
                        <button
                            id="copyBtn"
                            class="text-xs px-3 py-1 rounded-full border border-slate-700 text-slate-300 hover:bg-slate-800/80 disabled:opacity-40 disabled:cursor-not-allowed"
                            disabled
                        >
                            Copy
                        </button>
                    </div>

                    <div id="outputContainer"
                         class="mt-1 flex-1 rounded-xl bg-slate-950/70 border border-slate-800/80 overflow-hidden">
                        <pre id="output"
                             class="w-full h-full text-xs md:text-sm p-3 md:p-4 whitespace-pre-wrap break-words font-mono text-slate-200">
Ready to generate your plan. Describe your idea on the left and click “Generate Plan”.</pre>
                    </div>
                </section>
            </main>

            <footer class="mt-6 text-[11px] text-slate-500 flex flex-wrap items-center justify-between gap-2">
                <span>Copyright © 2025. For personal experimentation only.</span>
                <span>Built with FastAPI · Google ADK · Gemini</span>
            </footer>
        </div>

        <script>
            const generateBtn = document.getElementById("generateBtn");
            const copyBtn = document.getElementById("copyBtn");
            const ideaInput = document.getElementById("idea");
            const output = document.getElementById("output");
            const statusEl = document.getElementById("status");
            const btnIcon = document.getElementById("btnIcon");

            async function generatePlan() {
                const idea = ideaInput.value.trim();
                if (!idea) {
                    statusEl.textContent = "Please enter a business idea first.";
                    return;
                }

                generateBtn.disabled = true;
                copyBtn.disabled = true;
                statusEl.textContent = "Generating a long, formal business plan...";
                btnIcon.textContent = "⏳";
                output.textContent = "Thinking through market, strategy, and financials...";

                try {
                    const resp = await fetch("/generate", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ idea }),
                    });

                    if (!resp.ok) {
                        const err = await resp.json().catch(() => ({}));
                        throw new Error(err.error || `Request failed with status ${resp.status}`);
                    }

                    const data = await resp.json();
                    output.textContent = data.plan || "(No content returned from agent.)";
                    statusEl.textContent = "Plan generated successfully.";
                    copyBtn.disabled = false;
                } catch (e) {
                    console.error(e);
                    output.textContent = "Error while generating plan. Check server logs.";
                    statusEl.textContent = e.message || "Unexpected error.";
                } finally {
                    generateBtn.disabled = false;
                    btnIcon.textContent = "⚡";
                }
            }

            generateBtn.addEventListener("click", generatePlan);
            ideaInput.addEventListener("keydown", (e) => {
                if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
                    generatePlan();
                }
            });

            copyBtn.addEventListener("click", async () => {
                try {
                    await navigator.clipboard.writeText(output.textContent || "");
                    statusEl.textContent = "Copied plan to clipboard.";
                } catch (e) {
                    statusEl.textContent = "Could not copy to clipboard.";
                }
            });
        </script>
    </body>
    </html>
    """
)

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse(HTML_PAGE)


@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generate a long, formal business plan from the user's idea using the root agent.
    """

    idea = request.idea.strip()
    if not idea:
        return JSONResponse({"error": "Idea cannot be empty."}, status_code=400)

    # In a browser UI you typically want a stable user ID.
    user_id = "web_user"

    # Option 1: single long-lived session id
    # session_id = "web_session"
    # Option 2: per-request unique session to keep each generation isolated
    session_id = f"web_session_{uuid.uuid4()}"

    # --- IMPORTANT: Ensure the session exists BEFORE calling runner.run_async ---
    session = await session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
    )

    # Build content for ADK
    content = types.Content(
        role="user",
        parts=[types.Part(text=idea)],
    )

    final_chunks: list[str] = []

    # Stream all events from the agent run
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,  # use the ID from the created session
        new_message=content,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    final_chunks.append(part.text)

    if not final_chunks:
        return JSONResponse(
            {"error": "No final response content was produced by the agent."},
            status_code=500,
        )

    plan = "\n".join(final_chunks)
    return JSONResponse({"plan": plan})
