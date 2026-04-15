import os
from mistralai.client import Mistral


def ask_mistral(prompt: str):
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        return "ERROR: API key not found"

    try:
        with Mistral(api_key=api_key) as mistral:
            res = mistral.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )

            return res.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"
