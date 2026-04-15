import json
import httpx
import os
from app.mistral_client import ask_mistral


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


def search_web(query: str) -> str:
    """Search the web using Tavily API for real-time results."""
    if not TAVILY_API_KEY:
        return "No Tavily API key set — skipping web search."
    try:
        response = httpx.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": 8,
                "include_answer": True,
            },
            timeout=20,
        )
        data = response.json()
        results = data.get("results", [])
        lines = []
        for r in results:
            lines.append(f"- [{r.get('title', '')}]({r.get('url', '')}): {r.get('content', '')[:300]}")
        return "\n".join(lines) if lines else "No results found."
    except Exception as e:
        return f"Web search error: {str(e)}"


def search_github(query: str) -> str:
    """Search GitHub repos using public API (no auth needed for basic search)."""
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = httpx.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "sort": "stars", "order": "desc", "per_page": 8},
            headers=headers,
            timeout=20,
        )
        data = response.json()
        repos = data.get("items", [])
        lines = []
        for r in repos:
            lines.append(
                f"- {r['full_name']} ⭐{r['stargazers_count']} — {r.get('description', 'No description')} | {r['html_url']}"
            )
        return "\n".join(lines) if lines else "No GitHub results found."
    except Exception as e:
        return f"GitHub search error: {str(e)}"


def extract_tools_from_idea(idea: str) -> dict:
    """Use Mistral to extract domain keywords and tool categories from idea."""
    response = ask_mistral(f"""
You are a tech research assistant.

Given this idea/project description:
"{idea}"

Return a JSON object (no markdown, no explanation) with:
{{
  "domain": "the primary domain (e.g. computer vision, NLP, fintech, devtools)",
  "web_queries": ["2-3 specific search queries to find tools/APIs/frameworks"],
  "github_query": "one GitHub search query for relevant repos",
  "categories": ["list of tool categories to look for"]
}}
""")
    try:
        clean = response.strip().replace("```json", "").replace("```", "")
        return json.loads(clean)
    except Exception:
        return {
            "domain": "general",
            "web_queries": [f"best tools and frameworks for {idea}"],
            "github_query": idea,
            "categories": ["libraries", "APIs", "frameworks"]
        }


def run_research(idea: str) -> str:
    try:
        # STEP 1 — Extract structured intent from idea
        meta = extract_tools_from_idea(idea)
        domain = meta.get("domain", "general")
        web_queries = meta.get("web_queries", [f"best tools for {idea}"])
        github_query = meta.get("github_query", idea)
        categories = meta.get("categories", [])

        # STEP 2 — Web search (real-time)
        web_results = []
        for q in web_queries[:2]:  # max 2 queries to stay fast
            web_results.append(f"Query: {q}\n{search_web(q)}")
        web_combined = "\n\n".join(web_results)

        # STEP 3 — GitHub search
        github_results = search_github(github_query)

        # STEP 4 — Synthesize with Mistral
        final = ask_mistral(f"""
You are a senior tech researcher helping a developer find the best tools.

The developer's idea/project:
"{idea}"

Domain identified: {domain}
Categories to cover: {', '.join(categories)}

--- WEB SEARCH RESULTS ---
{web_combined}

--- GITHUB TRENDING REPOS ---
{github_results}

---

Based on ALL of the above, give a structured, actionable report:

## 🔧 Top Tools & Frameworks
For each tool:
- **Name** — what it does, why it's relevant, link if available

## 📦 Key Libraries / SDKs
List the most useful packages with brief descriptions.

## 🌐 APIs & Services
Any hosted services, APIs, or SaaS tools worth using.

## 🚀 Recommended Stack
A short opinionated recommendation for how to combine these.

Be specific. No generic advice. Focus on what actually exists and is production-ready.
""")

        return final

    except Exception as e:
        return f"ERROR: {str(e)}"