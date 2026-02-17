import time
from openai import OpenAI

def create_openai_client():
    """
    Create an OpenAI client object.

    NOTE: Replace "API KEY" with a secure method (e.g., environment variable)
    instead of hardcoding. Example:
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        return OpenAI(api_key=api_key)
    """
    return OpenAI(api_key="API KEY")  # <-- TEMP for testing only


def call_gpt_api(client, system_prompt, user_prompt, model="gpt-4o", max_retries=3):
    """
    Sends a prompt to the GPT model and returns the response text.

    Args:
        client: OpenAI client instance (from create_openai_client()).
        system_prompt (str): The "system" role instructions (rules for the model).
        user_prompt (str): The specific user input (e.g., article details).
        model (str): Model name, defaults to "gpt-4o".
        max_retries (int): Number of retries on error before giving up.

    Returns:
        str or None: The model's response text, or None if all retries fail.
    """

    # Format the conversation as required by the API
    messages = [
        {"role": "system", "content": system_prompt},  # system instructions
        {"role": "user", "content": user_prompt}       # user-provided input
    ]

    # Retry loop in case of temporary errors (rate limits, network issues, etc.)
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2  # low randomness = more consistent outputs
            )
            # Return only the content of the first choice
            return response.choices[0].message.content

        except Exception as e:
            print(f"[Error - Attempt {attempt + 1}] {e}")
            time.sleep(5)  # wait before retrying

    # If all retries failed, return None
    return None
