from mistralai.client import Mistral
import os


def ask_mistral(prompt: str, model: str = "mistral-small-latest") -> str:
    try:
        with Mistral(api_key=os.getenv("MISTRAL_API_KEY", "")) as mistral:
            res = mistral.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                response_format={"type": "text"},
            )
            return res.choices[0].message.content
    except Exception as e:
        return f"Mistral Error: {str(e)}"