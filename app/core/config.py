import os
from app.models.schemas import Language

class Settings:
    PROJECT_NAME: str = "HackerLearn Compiler"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    LANGUAGE_CONFIGS = {
        Language.PYTHON: {
            "extension": ".py",
            "compile_cmd": None,
            "run_cmd": ["python", "{file_path}"]
        },
        Language.C: {
            "extension": ".c",
            "compile_cmd": ["gcc", "{file_path}", "-o", "{executable_path}"],
            "run_cmd": ["{executable_path}"]
        },
        Language.CPP: {
            "extension": ".cpp",
            "compile_cmd": ["g++", "{file_path}", "-o", "{executable_path}"],
            "run_cmd": ["{executable_path}"]
        },
        Language.CSHARP: {
            "extension": ".cs",
            "compile_cmd": ["csc", "{file_path}", "-out:{executable_path}"],
            "run_cmd": ["mono", "{executable_path}"]
        }
    }

settings = Settings()