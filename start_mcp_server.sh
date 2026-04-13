#!/bin/bash

echo "====================================="
echo "  Virtura Content System MCP Server  "
echo "====================================="
echo ""

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误: Node.js 未安装"
    echo "请先安装 Node.js (https://nodejs.org/)"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: npm 未安装"
    echo "请先安装 Node.js (https://nodejs.org/)"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "mcp_server/package.json" ]; then
    echo "❌ 错误: 请在 virtura_content_system 根目录运行此脚本"
    exit 1
fi

echo "📦 检查并安装依赖..."
cd mcp_server
if [ ! -d "node_modules" ]; then
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 错误: 依赖安装失败"
        exit 1
    fi
fi

cd ..

echo ""
echo "✅ 依赖检查完成"
echo ""
echo "🚀 启动 Virtura Content System MCP 服务器..."
echo "   地址: http://127.0.0.1:8000"
echo "   按 Ctrl+C 停止服务器"
echo ""

cd mcp_server
npm start
