from app.mistral_client import ask_mistral


def run_research(idea: str):
    prompt = f"""
    You are a research assistant.
    Analyze this startup idea and provide:
    1. Industry
    2. Target audience
    3. Monetization ideas
    4. Challenges

    Idea: {idea}
    """

    return ask_mistral(prompt)
