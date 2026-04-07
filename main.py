
import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    parser = argparse.ArgumentParser(description="Generate content using Gemini API.")
    parser.add_argument("user_prompt", type=str, help="The prompt to generate content from.")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

    client = genai.Client(api_key=api_key)

    gen_content = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

    if gen_content.usage_metadata is None:
        raise RuntimeError("Usage metadata is not available in the response.")
    
    print(f"Prompt tokens: {gen_content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {gen_content.usage_metadata.candidates_token_count}")

    print(gen_content.text)


if __name__ == "__main__":
    main()
