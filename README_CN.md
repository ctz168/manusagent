# ManusAgent: 深度对齐 Manus 原生引擎的全源码复刻指南

本仓库是对 Manus 自主 AI Agent 容器内引擎的深度逆向与复刻成果。通过分析真实运行的 `sandbox-runtime` 和 `manus-mcp-server` 进程，我们提取了关键的系统编排脚本，并使用 Python 还原了原本闭源的二进制组件逻辑。

---

## 🏗 一、原生引擎全景架构 (1:1 对齐)

Manus Agent 引擎运行在 Ubuntu 22.04 容器中，采用 **Supervisor** 进行多层级服务编排。

### 1. 核心进程树
```text
systemd(1)
└── supervisord(699)
    ├── sandbox-runtime (8330端口) -> 执行核心 (start_server)
    ├── manus-mcp-server (stdin/stdout) -> 协议网关 (manus-mcp-cli)
    ├── code-server (8329端口) -> 可视化 IDE
    └── chrome/xvfb -> 浏览器执行环境
```

### 2. 指令流转逻辑
1. **云端大脑 (LLM)** 下达 JSON 指令。
2. **MCP 网关** (`manus_mcp_bridge_open.py`) 接收指令并解析。
3. **运行时执行** (`manus_runtime_open.py`) 接收 MCP 请求，通过 `asyncio.create_subprocess_shell` 在 Linux 沙箱中执行。
4. **结果回传**：执行结果（stdout/stderr）按原路回传给 LLM。

---

## 📂 二、核心组件与源码解析

本仓库已将原生环境中的明文源码与复刻逻辑分类存放：

### 1. 运行时层 (`runtime_layer/`)
- **`data_api.py`**: **[原生源码]** 用于沙箱内请求外部 API 的代理客户端。
- **`runtime_version.py`**: **[原生源码]** 记录当前引擎版本（v2.0.29）。
- **`start_server.sh`**: **[原生源码]** 核心运行时的启动脚本，包含复杂的 Python 环境变量配置。
- **`manus_runtime_open.py`**: **[开源重构]** 完美替代原生 `start_server` 二进制文件，提供 `/healthz` 和 `/execute` 接口。

### 2. 协议层 (`mcp_layer/`)
- **`start-manus-mcp-server.sh`**: **[原生源码]** 负责等待运行时就绪并拉起 MCP 服务。
- **`manus_mcp_bridge_open.py`**: **[开源重构]** 替代原生 `manus-mcp-cli`，实现标准的 MCP 协议交互逻辑。

### 3. 编排层 (`supervisor_conf/` & `scripts/`)
- **`1-sandbox-runtime.conf`**: **[原生配置]** 定义了核心运行时的启动优先级、用户权限和日志路径。
- **`11-manus-mcp-server.conf`**: **[原生配置]** 定义了协议网关的守护逻辑。
- **`7-code-server.conf`**: **[原生配置]** 定义了可视化 IDE 的启动逻辑。
- **`check-start-code-server.sh`**: **[原生脚本]** 包含动态生成密码和端口绑定的初始化逻辑。

---

## 🚀 三、实战部署与运行

### 1. 环境准备 (Ubuntu 22.04+)
```bash
# 安装核心依赖
sudo apt-get update && sudo apt-get install -y python3-pip curl supervisor
pip install fastapi uvicorn requests
```

### 2. 一键启动流程
1. **部署配置**: 将 `supervisor_conf/` 下的文件拷贝到 `/etc/supervisor/conf.d/`。
2. **启动引擎**:
   ```bash
   # 启动全源码版运行时
   python3 runtime_layer/manus_runtime_open.py &
   
   # 启动全源码版 MCP 桥接器
   python3 mcp_layer/manus_mcp_bridge_open.py
   ```
3. **验证连通性**:
   访问 `http://localhost:8330/healthz`，若返回 `{"status": "ok", "version": "2.0.29"}` 则表示引擎对齐成功。

---

## 🛠 四、开发者说明
本仓库旨在通过全源码化的方式，让开发者能够深入理解 Manus Agent 的底层运行机制。
- **二进制替代**: 我们使用 Python FastAPI 框架重写了 C++/Go 编写的二进制文件，在保证功能对齐的同时，提供了极高的可读性和二次开发能力。
- **环境变量**: 原生引擎重度依赖环境变量（见 `README_CN.md` 中的架构图说明），部署时请务必参考 `scripts/` 下的加载逻辑。

如果您有任何复现上的问题，欢迎在 GitHub 提交 Issue！
