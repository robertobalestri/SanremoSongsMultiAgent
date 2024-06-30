from crewai_tools import FileReadTool, DirectoryReadTool

file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool(directory='data/extracted')

from crewai_tools import BaseTool
import os

class write2fileTool(BaseTool):
    name: str = "Write to file"
    description: str = "Write the argument to a file"

    def _run(self, argument: str, file: str) -> str:
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file, 'w') as f:
            f.write(argument)
        return f"Result written to {file}"
    
write2file_tool = write2fileTool()