import os
import json
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import subprocess

app = FastAPI()

# 模拟健康检查接口，这是 Code-Server 和其他组件启动的前置条件
@app.get("/healthz")
async def health_check():
    return {"status": "ok", "version": "2.0.29-open-source"}

# 模拟 API 代理接口
@app.post("/apiproxy.v1.ApiProxyService/CallApi")
async def call_api(request: Request):
    data = await request.json()
    api_id = data.get("apiId")
    
    # 这里的逻辑是核心：它应该根据 apiId 调用外部服务或执行本地工具
    # 在开源版中，我们可以将其路由到本地的 Shell 执行或模拟返回
    print(f"[*] Received API Call: {api_id}")
    
    # 示例：如果是搜索 API，可以模拟返回（实际应对接搜索服务）
    if "search" in api_id.lower():
        return {
            "jsonData": json.dumps({
                "results": [{"title": "Manus Open Source Runtime", "url": "https://github.com/ctz168/manusagent"}]
            })
        }
    
    return {"jsonData": json.dumps({"message": f"API {api_id} executed in sandbox"})}

# 模拟工具执行接口 (由 MCP 调用)
@app.post("/execute")
async def execute_tool(request: Request):
    data = await request.json()
    command = data.get("command")
    
    print(f"[*] Executing Command: {command}")
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
    # 监听 8330 端口，这是 Manus 标准的运行时端口
    uvicorn.run(app, host="0.0.0.0", port=8330)
