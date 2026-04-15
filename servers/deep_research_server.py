import sys

def deep_analysis(query):
    return f"""
[Deep Research Layer]

Idea: {query}

- Core problem analysis
- Potential innovation areas
- Research directions
- Expansion opportunities
"""

if __name__ == "__main__":
    for line in sys.stdin:
        query = line.strip()
        print(deep_analysis(query))