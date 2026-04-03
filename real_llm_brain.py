import os
import json
import asyncio
import requests
import sys

# 这是一个实战版的“Manus 外部大脑”示例。
# 它展示了如何通过 OpenAI API (或其他兼容接口) 产生决策，
# 并通过 MCP 协议指挥沙箱身体 (manus_mcp_bridge.py) 执行任务。

# 配置项：请将这些填入您的真实 API Key 和地址
API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = "gpt-4-turbo-preview"

# 系统提示词：定义 Agent 的身份和工具使用规范
SYSTEM_PROMPT = """
你是一个名为 Manus 的自主 AI Agent。你运行在一个 Linux 沙箱环境中。
你可以通过发送 JSON 格式的 MCP 指令来操作这个环境。

目前支持的工具方法：
1. shell/run: 执行 shell 命令。参数: {"command": "你的命令"}

你的目标是：根据用户的要求，自主思考并执行必要的步骤。
每次执行完工具后，你会收到 stdout/stderr，请根据结果决定下一步行动。
"""

async def call_llm(messages):
    """调用大模型获取下一步决策"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"[!] LLM API 调用失败: {e}", file=sys.stderr)
        return None

async def execute_mcp_instruction(instruction_str):
    """将 LLM 产生的指令发送给 MCP 桥接器执行 (这里模拟通过 subprocess 管道调用)"""
    try:
        # 在真实部署中，这里应该与正在运行的 manus_mcp_bridge.py 进行进程间通信
        # 为了演示，我们直接调用本地 Python 逻辑
        process = await asyncio.create_subprocess_exec(
            "python3", "mcp_layer/manus_mcp_bridge.py",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate(input=instruction_str.encode())
        return stdout.decode()
    except Exception as e:
        return json.dumps({"error": str(e)})

async def main_loop(user_goal):
    """主思考循环：思考 -> 决策 -> 执行 -> 反思"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"我的目标是：{user_goal}"}
    ]
    
    print(f"[*] Manus Agent 启动，目标：{user_goal}")
    
    # 最多循环 5 次，防止死循环
    for i in range(5):
        print(f"\n[第 {i+1} 步思考中...]")
        llm_response = await call_llm(messages)
        if not llm_response: break
        
        print(f"[*] 大脑决策：{llm_response}")
        messages.append({"role": "assistant", "content": llm_response})
        
        # 尝试从 LLM 回复中提取 JSON 指令
        try:
            # 这里简单寻找 JSON 块，实战中可以使用正则或 Function Calling
            if "{" in llm_response and "}" in llm_response:
                start = llm_response.find("{")
                end = llm_response.rfind("}") + 1
                instruction = llm_response[start:end]
                
                print(f"[*] 正在执行指令：{instruction}")
                result = await execute_mcp_instruction(instruction)
                print(f"[*] 执行结果：{result.strip()}")
                
                messages.append({"role": "user", "content": f"工具执行结果如下：\n{result}"})
            else:
                print("[*] 任务似乎已完成，或 LLM 未产生有效指令。")
                break
        except Exception as e:
            print(f"[!] 解析指令失败: {e}")
            break

if __name__ == "__main__":
    if API_KEY == "your_api_key_here":
        print("[!] 警告：未检测到有效的 API Key。请在脚本中配置或设置环境变量。")
        sys.exit(1)
    
    goal = sys.argv[1] if len(sys.argv) > 1 else "查看当前系统信息并创建一个 hello.txt 文件"
    asyncio.run(main_loop(goal))
