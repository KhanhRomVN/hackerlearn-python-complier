from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Khởi tạo FastAPI và rate limiter
app = FastAPI(title="Python Code Compiler API")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class CodeRequest(BaseModel):
    code: str
    user_input: Optional[str] = None

@app.post("/compile")
@limiter.limit("20/minute")
async def compile_code(request: CodeRequest):
    try:
        # Tạo file tạm thời để lưu code
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as temp_file:
            temp_file.write(request.code)
            temp_file_path = temp_file.name

        try:
            if request.user_input:
                # Chạy code với input từ người dùng
                process = subprocess.Popen(
                    ['python3.9', temp_file_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(
                    input=request.user_input, 
                    timeout=5  # Timeout 5 giây
                )
            else:
                # Chạy code không cần input
                result = subprocess.run(
                    ['python3.9', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=5  # Timeout 5 giây
                )
                stdout = result.stdout
                stderr = result.stderr

            return {
                "status": "success",
                "output": stdout,
                "error": stderr
            }

        except subprocess.TimeoutExpired:
            raise HTTPException(
                status_code=408, 
                detail="Code execution timed out (limit: 5 seconds)"
            )
        finally:
            # Luôn xóa file tạm sau khi chạy xong
            os.unlink(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Python Code Compiler API",
        "endpoints": {
            "/compile": "POST - Compile and run Python code",
        },
        "limits": {
            "requests": "5 per minute per IP",
            "execution_time": "5 seconds",
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)