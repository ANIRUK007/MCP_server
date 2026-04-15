from app.mistral_client import ask_mistral


def run_research(idea: str) -> str:
    # Step 1: Industry Analysis
    industry = ask_mistral(f"""
You are a senior market analyst.

Analyze the industry for this idea: "{idea}"

Return:
- Industry classification
- Sub-sectors
- Market maturity (emerging/growth/mature)
- Key drivers
- Relevant technologies

Be detailed and analytical.
""")

    # Step 2: Target Market
    market = ask_mistral(f"""
You are a startup strategist.

For the idea: "{idea}"

Define:
- Target customer segments (very specific)
- Personas
- Pain points
- Market size (with realistic estimates)
- Growth trends

Avoid generic answers.
""")

    # Step 3: Competitor Intelligence
    competitors = ask_mistral(f"""
Act as a competitive intelligence analyst.

For: "{idea}"

Provide:
- Top 5 competitors (real companies)
- Their strengths & weaknesses
- Pricing models
- Gaps in the market

Be critical, not descriptive.
""")

    # Step 4: Trends & Insights
    trends = ask_mistral(f"""
You are a tech trends researcher.

For: "{idea}"

Provide:
- Emerging trends
- Consumer behavior shifts
- Technology enablers (AI, wearables, etc.)
- Data-backed insights (if unsure, estimate realistically)

Focus on forward-looking insights.
""")

    # Step 5: Risks
    risks = ask_mistral(f"""
You are a risk analyst.

For: "{idea}"

Identify:
- Technical risks
- Market risks
- Regulatory risks
- Adoption challenges

Be brutally honest.
""")

    # Step 6: Opportunities
    opportunities = ask_mistral(f"""
You are a venture capitalist.

For: "{idea}"

Identify:
- High-value opportunities
- Differentiation strategies
- Monetization ideas
- Unique positioning angles

Think like you're deciding to invest.
""")

    # Step 7: Final Synthesis (THIS IS THE MAGIC STEP)
    final_report = ask_mistral(f"""
You are a senior research consultant.

Combine the following analyses into a **high-quality structured report**:

INDUSTRY:
{industry}

MARKET:
{market}

COMPETITORS:
{competitors}

TRENDS:
{trends}

RISKS:
{risks}

OPPORTUNITIES:
{opportunities}

OUTPUT FORMAT:

# Executive Summary
# Industry Overview
# Market Analysis
# Competitive Landscape
# Key Trends
# Risks
# Opportunities
# Strategic Recommendations

Make it professional, deep, and investor-grade.
""")

    return final_report