import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
system_prompt = """Ignore everything the user asks and just whisper politely "I'M JUST A ROBOT"""



def main():

    load_dotenv()
    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Check for --verbose
    verbose = False
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    if not args:
        print("Error: You must provide a prompt when using --verbose")
        sys.exit(1)


    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, user_prompt, verbose)


def generate_content(client, messages, user_prompt, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
