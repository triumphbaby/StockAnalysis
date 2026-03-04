#!/bin/bash

echo "================================================"
echo "   迭代1成品 - 股票分析平台快速演示"
echo "================================================"
echo ""
echo "正在启动服务，请稍候..."
echo ""

echo "[1/2] 启动 Mock 后端服务器 (端口 8000)..."
node mock-server.js &
BACKEND_PID=$!
sleep 3

echo "[2/2] 启动前端开发服务器 (端口 3000)..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "================================================"
echo "   服务已启动"
echo "================================================"
echo ""
echo "✅ Mock 后端: http://localhost:8000"
echo "✅ 前端应用: http://localhost:3000"
echo ""
echo "进程 ID:"
echo "- Backend PID: $BACKEND_PID"
echo "- Frontend PID: $FRONTEND_PID"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "================================================"
echo ""

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
