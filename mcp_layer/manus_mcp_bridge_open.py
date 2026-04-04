import json
import asyncio
import sys
import os
import requests

# 模拟 manus-mcp-cli serve 的逻辑
# 它作为 MCP Server 运行，接收 stdin 指令并调用运行时

RUNTIME_URL = os.getenv("RUNTIME_URL", "http://localhost:8330")

async def handle_mcp_request(line):
    """处理 MCP 协议请求并调用 runtime 执行"""
    try:
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "shell/run":
            command = params.get("command")
            print(f"[*] MCP Executing: {command}", file=sys.stderr)
            
            # 调用本地 runtime
            resp = requests.post(f"{RUNTIME_URL}/execute", json={"command": command})
            resp.raise_for_status()
            result = resp.json()
            
            # 返回标准的 MCP JSON-RPC 格式
            return json.dumps({
                "id": req.get("id"),
                "result": {
                    "stdout": result.get("stdout", ""),
                    "stderr": result.get("stderr", ""),
                    "exit_code": result.get("exit_code", 0)
                }
            })
        
        elif method == "system/status":
            resp = requests.get(f"{RUNTIME_URL}/healthz")
            return json.dumps({
                "id": req.get("id"),
                "result": resp.json()
            })
            
        else:
            return json.dumps({
                "id": req.get("id"),
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
            
    except Exception as e:
        return json.dumps({"error": {"code": -32603, "message": str(e)}})

async def main():
    print("[*] Manus MCP Open Source Server Started (Listening on stdin)", file=sys.stderr)
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        
        response = await handle_mcp_request(line)
        print(response)
        sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
