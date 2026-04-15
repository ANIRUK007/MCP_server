# app/orchestrator.py

from app.mistral_client import ask_mistral


def run_research(idea: str) -> str:
    """
    Runs a fast research analysis using a single Mistral API call.
    This avoids Render timeout issues.
    """

    prompt = f"""
You are an expert startup analyst.

Analyze the following idea:
"{idea}"

Provide a concise but structured response with:

1. Industry:
   - What industry does this belong to?

2. Target Market:
   - Who are the customers?
   - Market size (rough estimate if possible)

3. Competitors:
   - List 3-5 competitors

4. Opportunities:
   - Key advantages or gaps in the market

5. Risks:
   - Main challenges or downsides

Keep it clear, structured, and under 200 words.
"""

    try:
        result = ask_mistral(prompt)
        return f"<pre>{result}</pre>"

    except Exception as e:
        return f"<h3>ERROR:</h3><pre>{str(e)}</pre>"