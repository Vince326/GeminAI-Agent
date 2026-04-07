
import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types



def generate_content(client, messages):
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    return response

def print_response(response):
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is not available in the response.")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    
def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate content using Gemini API.")
    parser.add_argument("user_prompt", type=str, help="The prompt to generate content from.")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    response = generate_content(client, messages)
    print_response(response)
    print(response.text)

if __name__ == "__main__":
    main()
