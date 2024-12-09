from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/compile")
async def compile_code(request: CodeRequest):
    try:
        # Tạo file tạm thời để lưu code
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as temp_file:
            temp_file.write(request.code)
            temp_file_path = temp_file.name

        # Chạy code bằng Python interpreter
        result = subprocess.run(
            ['python', temp_file_path],
            capture_output=True,
            text=True,
            timeout=5  # Giới hạn thời gian chạy là 5 giây
        )

        # Xóa file tạm
        os.unlink(temp_file_path)

        # Trả về kết quả
        return {
            "status": "success",
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Code execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)