import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from client import get_client

client = get_client()


def classify_email(email_text: str) -> str:
    """
    Step 1 — Classify the email into one of several categories.
    """

    messages = [
    {
        "role": "system",
        "content": (
            "You are an email classification assistant. "
            "Your job is to assign each email to exactly one category from this list: "
            "urgent, general_inquiry, support_request, sales_opportunity, spam_or_marketing."
        ),
    },
    {
        "role": "user",
        "content": (
            "Classify the following email. "
            "Respond with only the category name on a single line. Do not provide explanations.\n\n"
            f"Email:\n{email_text}"
        ),
    },
]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        category = response.choices[0].message.content.strip()
        return category
    except Exception as e:
        return f"Classification failed: {e}"


def generate_reply(email_text: str, category: str, tone: str = "professional") -> str:
    """
    Step 2 — Generate a reply based on category + tone.
    """

    messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful email response assistant. "
            "Your job is to generate clear, concise replies based on the email content, "
            "the classification category, and the desired tone. "
            "Always stay polite and professional, and avoid introducing new information "
            "that was not present in the original email."
        ),
    },
    {
        "role": "user",
        "content": (
            f"The email has been classified as: {category}.\n"
            f"Write a reply in a {tone} tone.\n\n"
            "Guidelines:\n"
            "- Keep the reply short (2–4 sentences).\n"
            "- Address the sender directly when appropriate.\n"
            "- Match the tone requested.\n"
            "- Base your response on the email content.\n\n"
            f"Original email:\n{email_text}"
        ),
    },
]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content
        return reply

    except Exception as e:
        return f"Reply generation failed: {e}"



if __name__ == "__main__":
    email = input("Paste email text:\n> ")
    tone = input("Choose reply tone (professional, friendly, concise): ")

    category = classify_email(email)
    reply = generate_reply(email, category, tone)

    print("\n--- Classification ---")
    print(category)

    print("\n--- Auto-Reply ---")
    print(reply)
