import sys
import json
import asyncio
import subprocess

# 这是一个模拟的 MCP (Model Context Protocol) 桥接器
# 它负责接收来自大模型 (LLM) 的 JSON 指令，并将其映射为本地 Shell 命令。

async def handle_request(line):
    try:
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        
        # 核心功能：执行 Shell 指令
        if method == "shell/run":
            command = params.get("command")
            print(f"[*] MCP Protocol - Running Shell: {command}", file=sys.stderr)
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            # 返回符合 MCP 标准的 JSON 响应
            result = {
                "id": req.get("id"),
                "result": {
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode(),
                    "exit_code": process.returncode
                }
            }
            print(json.dumps(result))
            sys.stdout.flush()
        
        # 获取系统状态
        elif method == "system/status":
            print(json.dumps({
                "id": req.get("id"),
                "result": {"status": "running", "agent": "Manus Open Source"}
            }))
            sys.stdout.flush()
            
        else:
            # 未知方法返回空结果
            print(json.dumps({"id": req.get("id"), "result": {}}))
            sys.stdout.flush()
            
    except Exception as e:
        print(f"[!] MCP Protocol Error: {str(e)}", file=sys.stderr)

async def main():
    print("[*] Manus Open Source MCP Bridge Started", file=sys.stderr)
    # 循环读取标准输入 (stdin)，这通常由 LLM 通过管道直接连接
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        await handle_request(line)

if __name__ == "__main__":
    asyncio.run(main())
