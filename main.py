from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
import sys

def main():
    load_dotenv()
    args=sys.argv[1:]
    verbose = '--verbose' in sys.argv
    argu=[]
    for arg in args:
        if not arg.startswith('--'):
            argu.append(arg)

    api_key = os.getenv("GEMINI_API_KEY")
    print(args)
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables!")

    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(argu)
   
    if verbose:
        print(f'user prompt :{user_prompt}')
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    


    def generate_content(client, messages):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
                )
        if verbose:
            print(f'ai response :{response.text}')
        else:    
            print(response.text ,response.usage_metadata.prompt_token_count,response.usage_metadata.candidates_token_count)
    generate_content(client, messages)
if __name__ == "__main__":
    main()
