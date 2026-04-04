#!/bin/sh
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_PATH=$(dirname "$SCRIPT")

PYTHONHOME=/home/ubuntu/.local/share/uv/python/cpython-3.13.8-linux-x86_64-gnu
export PYTHONHOME
NUITKA_PYTHONPATH="/opt/.manus/.sandbox-runtime/.venv/bin:/home/ubuntu/.local/share/uv/python/cpython-3.13.8-linux-x86_64-gnu/lib/python3.13:/home/ubuntu/.local/share/uv/python/cpython-3.13.8-linux-x86_64-gnu/lib/python3.13/lib-dynload:/opt/.manus/.sandbox-runtime/.venv/lib/python3.13/site-packages:/opt/.manus/.sandbox-runtime:/opt/.manus/.sandbox-runtime/.venv/lib/python3.13/site-packages/setuptools/_vendor"
export NUITKA_PYTHONPATH
PYTHONPATH="/opt/.manus/.sandbox-runtime/.venv/bin:/home/ubuntu/.local/share/uv/python/cpython-3.13.8-linux-x86_64-gnu/lib/python3.13:/home/ubuntu/.local/share/uv/python/cpython-3.13.8-linux-x86_64-gnu/lib/python3.13/lib-dynload:/opt/.manus/.sandbox-runtime/.venv/lib/python3.13/site-packages:/opt/.manus/.sandbox-runtime:/opt/.manus/.sandbox-runtime/.venv/lib/python3.13/site-packages/setuptools/_vendor"
export PYTHONPATH

"$SCRIPT_PATH/start_server" $@

