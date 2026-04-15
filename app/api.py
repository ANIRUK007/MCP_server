from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from app.orchestrator import run_research
import markdown

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>ToolScout — Find Your Stack</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #7c6af7;
    --accent2: #f76a8c;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --code-bg: #0d0d14;
    --radius: 12px;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 20px 100px;
  }

  /* Background grain texture */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  .container { width: 100%; max-width: 860px; position: relative; z-index: 1; }

  header { text-align: center; margin-bottom: 56px; }

  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 999px;
    padding: 4px 14px;
    margin-bottom: 20px;
    background: rgba(124,106,247,0.07);
  }

  h1 {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 16px;
    background: linear-gradient(135deg, #e8e8f0 0%, var(--accent) 60%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
  }

  .search-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 40px;
    box-shadow: 0 0 80px rgba(124,106,247,0.06);
  }

  label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
  }

  textarea {
    width: 100%;
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    padding: 16px 18px;
    resize: vertical;
    min-height: 120px;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
  }

  textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(124,106,247,0.15);
  }

  textarea::placeholder { color: var(--muted); }

  .btn {
    margin-top: 16px;
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border: none;
    border-radius: var(--radius);
    color: #fff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    letter-spacing: 0.02em;
    transition: opacity 0.2s, transform 0.15s;
    position: relative;
    overflow: hidden;
  }

  .btn:hover { opacity: 0.92; transform: translateY(-1px); }
  .btn:active { transform: translateY(0); }

  .btn::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(rgba(255,255,255,0.08), transparent);
  }

  /* Loading state */
  .loading {
    display: none;
    text-align: center;
    padding: 60px 0;
    color: var(--muted);
  }

  .spinner {
    width: 36px; height: 36px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* Results */
  .results-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px 40px;
    box-shadow: 0 0 80px rgba(124,106,247,0.06);
    animation: fadeUp 0.4s ease;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .results-card h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 24px;
    color: var(--accent);
  }

  /* Markdown rendered output */
  .result-body h2 {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 28px 0 12px;
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }

  .result-body h3 {
    font-size: 1rem;
    font-weight: 600;
    margin: 20px 0 8px;
    color: var(--text);
  }

  .result-body p {
    color: #c0c0d0;
    line-height: 1.7;
    margin-bottom: 12px;
    font-size: 0.95rem;
  }

  .result-body ul, .result-body ol {
    padding-left: 1.4em;
    margin-bottom: 16px;
  }

  .result-body li {
    color: #c0c0d0;
    line-height: 1.7;
    margin-bottom: 8px;
    font-size: 0.95rem;
  }

  .result-body strong {
    color: var(--text);
    font-weight: 600;
  }

  .result-body a {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid rgba(124,106,247,0.3);
  }

  .result-body a:hover {
    border-bottom-color: var(--accent);
  }

  .result-body code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 6px;
    color: var(--accent2);
  }

  .result-body pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    overflow-x: auto;
    margin-bottom: 16px;
  }

  .result-body pre code {
    background: none;
    border: none;
    padding: 0;
    color: #b8b8d0;
  }

  .error-box {
    background: rgba(247,106,140,0.08);
    border: 1px solid rgba(247,106,140,0.25);
    border-radius: var(--radius);
    padding: 20px;
    color: var(--accent2);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
  }

  footer {
    margin-top: 60px;
    text-align: center;
    color: var(--muted);
    font-size: 0.8rem;
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="badge">⚡ Powered by Mistral + MCP</div>
    <h1>ToolScout</h1>
    <p class="subtitle">Describe your idea — get the best tools, frameworks, and APIs to build it.</p>
  </header>

  <div class="search-card">
    <form id="researchForm" action="/research" method="post">
      <label for="idea">Your Project Idea</label>
      <textarea
        id="idea"
        name="idea"
        placeholder="e.g. A real-time fitness coaching app that uses pose detection to analyze workout form..."
        required
      ></textarea>
      <button type="submit" class="btn" id="submitBtn">
        🔍 &nbsp; Find My Stack
      </button>
    </form>
  </div>

  <div class="loading" id="loading">
    <div class="spinner"></div>
    <p>Researching tools across the web and GitHub...</p>
  </div>

  {RESULTS_BLOCK}
</div>

<footer>ToolScout — MCP Research Agent</footer>

<script>
  document.getElementById('researchForm').addEventListener('submit', function() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('submitBtn').textContent = 'Researching...';
  });
</script>
</body>
</html>
"""


def render_results(result_html: str, is_error: bool = False) -> str:
    if is_error:
        block = f'<div class="results-card"><div class="error-box">{result_html}</div></div>'
    else:
        block = f"""
        <div class="results-card">
          <div class="result-body">{result_html}</div>
        </div>
        """
    return block


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE.replace("{RESULTS_BLOCK}", "")


@app.post("/research", response_class=HTMLResponse)
def research(idea: str = Form(...)):
    result = run_research(idea)

    is_error = result.startswith("ERROR:")
    if is_error:
        results_block = render_results(result, is_error=True)
    else:
        result_html = markdown.markdown(result, extensions=["fenced_code", "tables"])
        results_block = render_results(result_html)

    page = HTML_PAGE.replace("{RESULTS_BLOCK}", results_block)
    # Pre-fill the textarea with the submitted idea
    page = page.replace(
        'placeholder="e.g.',
        f'value="{idea}" placeholder="e.g.'
    ).replace("<textarea", f'<textarea').replace(
        "</textarea>", f"{idea}</textarea>"
    )
    return page