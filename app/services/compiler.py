import os
import asyncio
import tempfile
from app.models.schemas import Language
from app.core.config import settings

class CompilerService:
    @staticmethod
    async def execute_code(code: str, language: Language, inputs: list[str] = None) -> tuple[str, str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source file
            file_path = os.path.join(temp_dir, f"main{settings.LANGUAGE_CONFIGS[language]['extension']}")
            with open(file_path, "w") as f:
                f.write(code)
            
            executable_path = os.path.join(temp_dir, "program")
            
            # Compile if needed
            if compile_cmd := settings.LANGUAGE_CONFIGS[language]["compile_cmd"]:
                compile_cmd = [
                    arg.format(file_path=file_path, executable_path=executable_path)
                    for arg in compile_cmd
                ]
                process = await asyncio.create_subprocess_exec(
                    *compile_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                _, stderr = await process.communicate()
                if process.returncode != 0:
                    return "", stderr.decode()
            
            # Run the program
            run_cmd = [
                arg.format(file_path=file_path, executable_path=executable_path)
                for arg in settings.LANGUAGE_CONFIGS[language]["run_cmd"]
            ]
            
            process = await asyncio.create_subprocess_exec(
                *run_cmd,
                stdin=asyncio.subprocess.PIPE if inputs else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Handle input if provided
            if inputs:
                input_data = "\n".join(inputs).encode()
                stdout, stderr = await process.communicate(input_data)
            else:
                stdout, stderr = await process.communicate()
            
            return stdout.decode(), stderr.decode()