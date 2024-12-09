import time
from fastapi import APIRouter, Request
from app.models.schemas import CodeRequest, CompileResponse
from app.services.compiler import CompilerService
from app.core.security import limiter

router = APIRouter()

@router.post("/compile", response_model=CompileResponse)
@limiter.limit("20/minute")
async def compile_code(request: Request, code_request: CodeRequest):
    start_time = time.time()
    
    stdout, stderr = await CompilerService.execute_code(
        code_request.code,
        code_request.language,
        code_request.inputs
    )
    
    execution_time = time.time() - start_time

    return CompileResponse(
        status="success",
        output=stdout,
        error=stderr,
        execution_time=round(execution_time, 3)
    )