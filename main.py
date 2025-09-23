import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv("key.env")
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) < 2:
        print("Error: No prompt provided.")
        sys.exit(1)

    user_prompt_parts = []
    verbose = False

    # Check for --verbose flag
    for arg in sys.argv[1:]:
        if arg == "--verbose":
            verbose = True
        else:
            user_prompt_parts.append(arg)

    user_prompt = " ".join(user_prompt_parts)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print(f"User prompt: {user_prompt}")

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )
    print(response.text)

    if response.usage_metadata:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        if verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
    else:
        if verbose: # Only print this if verbose is enabled and metadata is missing
            print("Usage metadata not available for this response.")

if __name__ == "__main__":
    main()