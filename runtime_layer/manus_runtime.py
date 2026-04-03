import os
import json
import asyncio
from fastapi import FastAPI, Request
import uvicorn
import subprocess

app = FastAPI()

# 1. 健康检查接口：这是 Code-Server 和 MCP 组件启动的前置依赖
@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "2.0.29-open-source"}

# 2. API 代理接口：模拟 CallApi 转发逻辑
@app.post("/apiproxy.v1.ApiProxyService/CallApi")
async def call_api(request: Request):
    data = await request.json()
    api_id = data.get("apiId")
    print(f"[*] API Proxy Call: {api_id}")
    # 模拟返回成功
    return {"jsonData": json.dumps({"status": "success", "message": f"API {api_id} executed"})}

# 3. 工具执行接口：供 MCP 或其他组件调用以执行 Shell 命令
@app.post("/execute")
async def execute_tool(request: Request):
    data = await request.json()
    command = data.get("command")
    print(f"[*] Executing: {command}")
    
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
    # 监听 8330 端口，这是 Manus 的标准运行时端口
    uvicorn.run(app, host="0.0.0.0", port=8330)
