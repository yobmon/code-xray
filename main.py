from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
import sys
from functions.get_files_info import schema_get_files_info
from functions.python_runner import schema_run_python
from functions.write_file_content import schema_write_file
from functions.file_content import schema_file_content
from fun_handler.func_handler import call_function
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

    
    system_prompt=system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


    available_functions = types.Tool(
        function_declarations=[
              schema_get_files_info,
              schema_file_content,
              schema_run_python,
              schema_write_file
          ]
    )




    














    def generate_content(client, messages, verbose=False):
      response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

      for candidate in response.candidates:
        ai_message = candidate.content
      
        messages.append(ai_message) 
        print(ai_message)
        print('message   --is')
        print(messages)
        if verbose:
            print(f"AI candidate response: {ai_message}")

        function_calls = [
            part.function_call for part in ai_message.parts if part.function_call
        ]

        if function_calls:
            for fc in function_calls:
                if verbose:
                    print(f"Calling function: {fc.name} with args {fc.args}")

                function_call_result = call_function(fc, verbose)

                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")

                result_msg = types.Content(
                    role="user",
                    parts=[function_call_result.parts[0]]
                )
                print('message here')
                
                messages.append(result_msg)
                print(messages)
                if verbose:
                    print(f"-> Function response: {function_call_result.parts[0].function_response.response}")

                return generate_content(client, messages, verbose)

        return response.candidates[0].content if response.candidates else None

    generate_content(client, messages)
if __name__ == "__main__":
    main()
