#!/usr/bin/env python3
"""
GitHub API 示例：使用 PyGithub 操作仓库
"""

from github import Github

# 使用个人访问令牌认证
# g = Github("your_personal_access_token")

# 或者使用环境变量
import os
token = os.environ.get("GITHUB_TOKEN")
g = Github(token) if token else Github()

# 获取公开仓库
repo = g.get_repo("github/gitignore")
print(f"Repository: {repo.full_name}")
print(f"Stars: {repo.stargazers_count}")
print(f"Description: {repo.description}")