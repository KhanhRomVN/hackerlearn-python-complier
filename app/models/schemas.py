from enum import Enum
from pydantic import BaseModel
from typing import List

class Language(str, Enum):
    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"

class CodeRequest(BaseModel):
    code: str
    language: Language
    inputs: List[str] = []

class CompileResponse(BaseModel):
    status: str
    output: str
    error: str
    execution_time: float