def industry_prompt(idea):
    return f"""
Analyze the industry relevance, competitors, and market demand for:
{idea}

Return structured bullet points.
"""

def methodology_prompt(idea):
    return f"""
List best methodologies, frameworks, and approaches used to build:
{idea}
"""

def tools_prompt(idea):
    return f"""
List tools, technologies, and tech stack required for:
{idea}
"""

def architecture_prompt(idea):
    return f"""
Suggest system architecture and technical design for:
{idea}
"""

def ui_prompt(idea):
    return f"""
Suggest UI/UX patterns and interface ideas for:
{idea}
"""