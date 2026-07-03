
import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function



def verbose_print(response, user_prompt, verbose):
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    
def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages,config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0))

    if response.usage_metadata is None:
       raise RuntimeError("Gemini API appears to be malformed.")
    # if response.function_calls is None:
    #     print(response.text)
    # else:
    #     function_responses = []
    #     for function_call in response.function_calls:
    #         result = call_function(function_call, verbose=verbose)
    #         if not result.parts:
    #             raise RuntimeError("Empty parts")
    #         if not result.parts[0].function_response:
    #             raise RuntimeError("No function response")
    #         if not result.parts[0].function_response.response:
    #             raise RuntimeError("No response data")
    #         if verbose:
    #                 print(f"-> {result.parts[0].function_response.response}")
    #         function_responses.append(result.parts[0])

    # verbose_print(response, args.user_prompt, args.verbose)

    return response


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate content using Gemini API.")
    parser.add_argument("user_prompt", type=str, help="The prompt to generate content from.")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output.")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
 #Loop makes the agent remember the conversation
    for _ in range(20):
        response = generate_content(client, messages, verbose=args.verbose)
        messages.append(response.candidates[0].content)

        if response.function_calls is None:
            print(response.text)
            break
        else:
           for function_call in response.function_calls:
               result_message = call_function(function_call, args.verbose)
               messages.append(result_message)
    else:
        print("Maximum iterations reached without a final response.")
        sys.exit(1)

if __name__ == "__main__":
    main()
