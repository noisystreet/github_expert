#!/bin/bash
# 预提交检查脚本：验证 RST 语法

set -e

echo "Checking RST syntax..."

# 检查是否有 sphinx-build 命令
if ! command -v sphinx-build &> /dev/null; then
    echo "Warning: sphinx-build not found, skipping RST check"
    exit 0
fi

# 运行 Sphinx 语法检查
sphinx-build -W -b html source _build/check 2>&1 | grep -i "warning\|error" || echo "No RST syntax errors found"

echo "Pre-commit check completed"