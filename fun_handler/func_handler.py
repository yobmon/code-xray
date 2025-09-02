from google.genai import types

from functions.get_files_info import schema_get_files_info,get_file_info
from functions.python_runner import schema_run_python,python_file_runner
from functions.write_file_content import schema_write_file,write_file
from functions.file_content import schema_file_content,get_file_content


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    func_map={
        'get_file_info':get_file_info,
        'get_file_content':get_file_content,
        'python_file_runner':python_file_runner,
        'write_file':write_file
    }
    function_name=function_call_part.name
    
    if function_name not in func_map:
        print('bug here') 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    working_dir="./calculator_test_agent"
    args =dict(function_call_part.args)
    args['working_directory']=working_dir
    function_result = func_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    ) 