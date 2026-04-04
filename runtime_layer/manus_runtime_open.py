import os
import json
import asyncio
import subprocess
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Any, Optional
import uvicorn

app = FastAPI(title="Manus Sandbox Runtime (Open Source)")

class ExecuteRequest(BaseModel):
    command: str
    cwd: Optional[str] = "/home/ubuntu"
    timeout: Optional[int] = 300

@app.get("/healthz")
async def health_check():
    """与原生 start_server 对齐的健康检查接口"""
    return {"status": "ok", "version": "2.0.29"}

@app.post("/execute")
async def execute_command(req: ExecuteRequest):
    """模拟原生执行接口，支持异步 shell 执行"""
    try:
        process = await asyncio.create_subprocess_shell(
            req.command,
            cwd=req.cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=req.timeout)
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit_code": process.returncode
        }
    except asyncio.TimeoutError:
        return {"error": "Execution timed out", "exit_code": -1}
    except Exception as e:
        return {"error": str(e), "exit_code": -1}

@app.post("/apiproxy.v1.ApiProxyService/CallApi")
async def call_api(request: Request):
    """对齐 data_api.py 的代理调用接口"""
    data = await request.json()
    # 在真实复刻中，这里应转发到 Manus 云端或本地模拟服务
    print(f"[*] API Call: {data.get('apiId')}")
    return {"jsonData": json.dumps({"status": "mocked", "message": "API Proxy reached"})}

if __name__ == "__main__":
    # 与原生端口 8330 对齐
    uvicorn.run(app, host="0.0.0.0", port=8330)
