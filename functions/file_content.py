import os

def get_file_content(working_directory, file_path):  
      
    abs_working_dir = os.path.abspath(working_directory)

    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the working directory' 
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path,'r') as file:
           content=file.read()
        if len(content)>10000:
           content=content[:10000]
           return f'{content} in   {file_path} this file is truncated to 10,000line'
        return content
    except Exception as e:
        return  f"Error displaying content: {e}" 
    