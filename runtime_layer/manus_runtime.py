import os
import json
import asyncio
from fastapi import FastAPI, Request
import uvicorn
import subprocess

app = FastAPI()

# 模拟健康检查接口
@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "2.0.29-open-source"}

# 模拟 API 代理接口
@app.post("/apiproxy.v1.ApiProxyService/CallApi")
async def call_api(request: Request):
    data = await request.json()
    api_id = data.get("apiId")
    print(f"[*] Calling API Proxy: {api_id}")
    # 在实际部署中，这里应该对接真实的外部 API 网关
    return {"jsonData": json.dumps({"status": "success", "apiId": api_id})}

# 工具执行接口 (由 MCP 调用)
@app.post("/execute")
async def execute_tool(request: Request):
    data = await request.json()
    command = data.get("command")
    print(f"[*] Executing command: {command}")
    
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit_code": process.returncode
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8330)
