import sys
import json
import asyncio
import subprocess

async def handle_request(line):
    try:
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        
        # 模拟 MCP 标准的 shell 运行方法
        if method == "shell/run":
            command = params.get("command")
            print(f"[*] MCP Execution: {command}", file=sys.stderr)
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
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
        else:
            # 对于其他请求，模拟返回空结果
            print(json.dumps({"id": req.get("id"), "result": {}}))
            sys.stdout.flush()
    except Exception as e:
        print(f"[!] Error: {str(e)}", file=sys.stderr)

async def main():
    print("[*] Open Source MCP Bridge Started", file=sys.stderr)
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        await handle_request(line)

if __name__ == "__main__":
    asyncio.run(main())
