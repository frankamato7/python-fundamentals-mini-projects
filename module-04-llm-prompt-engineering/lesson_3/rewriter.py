import os
import sys

# Ensure the parent directory (module-04-llm-prompt-engineering) is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from client import get_client

# Initialize the client
client = get_client()


def rewrite_text(text: str, style: str = "professional") -> str:
    """
    Rewrite the given text into a new style.
    - text: the original content
    - style: the desired tone or writing style
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert rewriting assistant. "
                "Your job is to rewrite text while preserving the intended meaning of the text. "
                "Follow the writing style that the user specifies with precision and accuracy."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Rewrite the text with a {style} style. "
                "Format the output as numbered points. "
                "Keep each numbered point to 1-3 sentences and make the text easy to skim.\n\n"
                "Do not introduce new ideas not present in the original text.\n\n"
                f"Original text:\n{text}"
            ),
        },
]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        rewritten = response.choices[0].message.content
        return rewritten

    except Exception as e:
        return f"Rewriting failed: {e}"
    


if __name__ == "__main__":
    print("Paste text to rewrite (single paragraph is fine):")
    text = input("> ")

    style = input("Enter desired style (e.g., professional, casual, friendly): ")

    rewritten = rewrite_text(text, style)

    print("\n--- Rewritten Text ---")
    print(rewritten)
