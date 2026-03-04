@echo off
chcp 65001 >nul
echo ================================================
echo    迭代1成品 - 股票分析平台快速演示
echo ================================================
echo.
echo 正在启动服务，请稍候...
echo.

echo [1/2] 启动 Mock 后端服务器 (端口 8000)...
start "Mock Backend Server" cmd /k "node mock-server.js"
timeout /t 3 /nobreak >nul

echo [2/2] 启动前端开发服务器 (端口 3000)...
cd frontend
start "Frontend Dev Server" cmd /k "npm start"

echo.
echo ================================================
echo    服务启动中...
echo ================================================
echo.
echo ✅ Mock 后端: http://localhost:8000
echo ✅ 前端应用: http://localhost:3000
echo.
echo 提示：
echo - 浏览器将自动打开前端应用
echo - 如需停止服务，关闭对应的命令窗口即可
echo - 详细使用说明请查看 START_DEMO.md
echo.
echo ================================================
pause
