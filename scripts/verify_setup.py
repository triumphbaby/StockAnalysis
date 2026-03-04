#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Setup Verification Script
验证项目基础设施是否正确配置
"""

import os
import sys
from pathlib import Path

# Simple markers without color codes for Windows compatibility
OK_MARK = "[OK]"
FAIL_MARK = "[FAIL]"
WARN_MARK = "[WARN]"


def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"{OK_MARK} {description}: {file_path}")
        return True
    else:
        print(f"{FAIL_MARK} {description}: {file_path} NOT FOUND")
        return False


def check_directory_exists(dir_path: str, description: str) -> bool:
    """Check if a directory exists"""
    if Path(dir_path).is_dir():
        print(f"{OK_MARK} {description}: {dir_path}")
        return True
    else:
        print(f"{FAIL_MARK} {description}: {dir_path} NOT FOUND")
        return False


def main():
    """Main verification function"""
    print("=" * 60)
    print("Stock Analysis Platform - Setup Verification")
    print("=" * 60)
    print()

    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    all_checks_passed = True

    # 1. Check core files
    print("1. Checking Core Configuration Files...")
    core_files = [
        (".env", "Environment variables file"),
        (".env.example", "Environment template file"),
        (".gitignore", "Git ignore file"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "Project README"),
    ]

    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    print()

    # 2. Check backend files
    print("2. Checking Backend Files...")
    backend_files = [
        ("backend/Dockerfile", "Backend Dockerfile"),
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/pytest.ini", "Pytest configuration"),
        ("backend/init.sql", "Database initialization script"),
        ("backend/app/__init__.py", "Backend app init"),
        ("backend/app/main.py", "FastAPI main application"),
        ("backend/app/config.py", "Backend configuration"),
        ("backend/app/database.py", "Database configuration"),
        ("backend/app/cache.py", "Redis cache manager"),
        ("backend/app/tasks.py", "Celery tasks"),
    ]

    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    print()

    # 3. Check backend test files
    print("3. Checking Backend Test Files...")
    test_files = [
        ("backend/tests/__init__.py", "Tests init"),
        ("backend/tests/conftest.py", "Pytest fixtures"),
        ("backend/tests/test_main.py", "Main API tests"),
        ("backend/tests/test_database.py", "Database tests"),
        ("backend/tests/test_cache.py", "Cache tests"),
    ]

    for file_path, description in test_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    print()

    # 4. Check frontend files
    print("4. Checking Frontend Files...")
    frontend_files = [
        ("frontend/Dockerfile", "Frontend Dockerfile"),
        ("frontend/package.json", "NPM dependencies"),
        ("frontend/tsconfig.json", "TypeScript configuration"),
        ("frontend/public/index.html", "HTML template"),
        ("frontend/public/manifest.json", "Web manifest"),
        ("frontend/src/index.tsx", "Frontend entry point"),
        ("frontend/src/App.tsx", "Main App component"),
        ("frontend/src/App.css", "App styles"),
        ("frontend/src/App.test.tsx", "App tests"),
        ("frontend/src/services/api.ts", "API service"),
    ]

    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    print()

    # 5. Check required directories
    print("5. Checking Required Directories...")
    required_dirs = [
        ("backend", "Backend directory"),
        ("backend/app", "Backend app directory"),
        ("backend/tests", "Backend tests directory"),
        ("frontend", "Frontend directory"),
        ("frontend/src", "Frontend source directory"),
        ("frontend/public", "Frontend public directory"),
    ]

    for dir_path, description in required_dirs:
        if not check_directory_exists(dir_path, description):
            all_checks_passed = False
    print()

    # 6. Check environment variables
    print("6. Checking Environment Variables...")
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()

        critical_vars = [
            "DATABASE_URL",
            "REDIS_URL",
            "OPENAI_API_KEY",
            "TUSHARE_TOKEN",
        ]

        for var in critical_vars:
            if var in env_content:
                # Check if it's not a placeholder
                if f"{var}=your_" in env_content or f"{var}=" in env_content and "=\n" in env_content:
                    print(f"{WARN_MARK} {var} is set but may be a placeholder")
                else:
                    print(f"{OK_MARK} {var} is configured")
            else:
                print(f"{FAIL_MARK} {var} is missing")
                all_checks_passed = False
    print()

    # Summary
    print("=" * 60)
    if all_checks_passed:
        print(f"{OK_MARK} All checks passed!")
        print("\nNext steps:")
        print("1. Make sure Docker Desktop is running")
        print("2. Run: docker-compose up -d")
        print("3. Wait for services to start (about 30-60 seconds)")
        print("4. Access frontend at: http://localhost:3000")
        print("5. Access API docs at: http://localhost:8000/docs")
        return 0
    else:
        print(f"{FAIL_MARK} Some checks failed!")
        print("\nPlease fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
