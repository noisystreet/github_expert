GitHub API
==========

上一节我们学习了 GitHub CLI——命令行工具提高操作效率。但 CLI 是预定义的命令，灵活性有限。如果需要更复杂的操作，比如批量处理、数据分析、自定义集成，需要使用 GitHub API。

API（Application Programming Interface）是程序访问 GitHub 的接口。通过 API，你可以用代码完成任何网页能做的操作，甚至更多。

两种 API：REST 与 GraphQL
-------------------------

GitHub 提供两种 API：REST API 和 GraphQL API。

**REST API**

REST API 是传统的 HTTP API。每个资源（仓库、Issue、PR）有对应的 URL，通过 HTTP 方法（GET、POST、PUT、DELETE）操作。

示例：

.. code-block:: bash

   # 获取仓库信息
   GET https://api.github.com/repos/owner/repo
   
   # 创建 Issue
   POST https://api.github.com/repos/owner/repo/issues
   {
     "title": "Bug report",
     "body": "Description"
   }

REST API 的特点：

- 直观：每个 URL 对应一个资源
- 简单：学习成本低，适合新手
- 广泛：几乎所有 GitHub 功能都有 REST API

**GraphQL API**

GraphQL API 是灵活的查询语言。你指定需要的数据，API 返回精确结果。

示例：

.. code-block:: json

   {
     repository(owner: "owner", name: "repo") {
       name
       description
       issues(first: 10) {
         totalCount
         nodes {
           title
           state
         }
       }
     }
   }

GraphQL API 的特点：

- 灵活：一次请求获取多个资源
- 高效：避免过度获取（over-fetching）或不足获取（under-fetching）
- 现代：适合复杂查询和前端应用

**选择哪种 API**

- **REST API**：适合简单操作、快速原型、新手入门
- **GraphQL API**：适合复杂查询、性能优化、前端应用

本节主要介绍 REST API，最后简要介绍 GraphQL。

REST API 基础
-------------

**API 结构**

REST API 的基本 URL：

::

   https://api.github.com

资源路径：

::

   /repos/{owner}/{repo}  # 仓库
   /repos/{owner}/{repo}/issues  # Issue
   /repos/{owner}/{repo}/pulls  # PR
   /repos/{owner}/{repo}/actions/runs  # 工作流运行
   /users/{username}  # 用户
   /orgs/{org}  # 组织

HTTP 方法：

.. list-table:: HTTP 方法与操作
   :widths: 20 80
   :header-rows: 1

   * - 方法
     - 操作
   * - GET
     - 获取资源（读取）
   * - POST
     - 创建资源（写入）
   * - PUT
     - 更新资源（修改）
   * - DELETE
     - 删除资源
   * - PATCH
     - 部分更新

**认证**

大部分 API 需要认证。未认证的请求：

- 只能访问公开资源
- 速率限制更严格（每小时 60 次）
- 无法写入

认证方式有三种：Personal Access Token、OAuth App、GitHub App。

**Personal Access Token（PAT）**

最简单的认证方式。创建 Token：

1. GitHub 设置页面 → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 选择权限范围（repo、issue、workflow 等）
4. 生成 Token（只显示一次，保存好）

使用 Token 认证：

.. code-block:: bash

   curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/user

或使用 Python：

.. code-block:: python

   import requests
   
   headers = {"Authorization": "token YOUR_TOKEN"}
   response = requests.get("https://api.github.com/user", headers=headers)
   print(response.json())

**OAuth App**

OAuth App 适合第三方应用。用户授权后，应用获得临时 Token。

OAuth 流程：

1. 应用引导用户到 GitHub 授权页面
2. 用户授权后，GitHub 返回授权码
3. 应用用授权码换取 Token
4. 应用使用 Token 访问用户资源

OAuth App 的特点：

- 用户可控：用户决定授权范围
- 安全：Token 可随时撤销
- 适用场景：第三方应用（如 CI 工具、桌面应用）

**GitHub App**

GitHub App 是现代的认证方式。比 OAuth App 更精细：

- 细粒度权限：可控制单个仓库的访问权限
- 短期 Token：Token 有效期短，更安全
- 安装式：用户安装 App 到仓库或组织

GitHub App 的特点：

- 安全性高：短期 Token、细粒度权限
- 适合场景：企业集成、自动化工具

创建 GitHub App：

1. GitHub 设置页面 → Developer settings → GitHub Apps
2. 点击 "New GitHub App"
3. 配置权限、回调 URL、Webhook
4. 生成 Private Key（用于 JWT 认证）

**速率限制**

API 有速率限制，防止滥用。

认证用户的限制：

::

   每小时 5000 次请求

未认证用户的限制：

::

   每小时 60 次请求

检查速率限制：

.. code-block:: bash

   curl -I https://api.github.com/user
   # 输出：
   # X-RateLimit-Limit: 5000
   # X-RateLimit-Remaining: 4999
   # X-RateLimit-Reset: 1705300000

- ``X-RateLimit-Limit``：总限制
- ``X-RateLimit-Remaining``：剩余次数
- ``X-RateLimit-Reset``：限制重置时间（Unix 时间戳）

超出限制会返回 403 错误：

.. code-block:: bash

   HTTP/1.1 403 Forbidden
   {
     "message": "API rate limit exceeded",
     "documentation_url": "https://docs.github.com/rest/rate-limit"
   }

应对速率限制：

- 检查 ``X-RateLimit-Remaining``，避免超限
- 超限后等待 ``X-RateLimit-Reset`` 时间
- 使用缓存减少重复请求
- 使用 GraphQL 一次获取多个资源，减少请求次数

常用 API 操作
-------------

**仓库操作**

获取仓库信息：

.. code-block:: bash

   curl https://api.github.com/repos/owner/repo

响应：

.. code-block:: json

   {
     "name": "repo",
     "full_name": "owner/repo",
     "description": "My repository",
     "private": false,
     "html_url": "https://github.com/owner/repo",
     "stargazers_count": 123,
     "forks_count": 45,
     "open_issues_count": 10
   }

创建仓库：

.. code-block:: bash

   curl -X POST \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"name":"new-repo","private":true}' \
     https://api.github.com/user/repos

更新仓库：

.. code-block:: bash

   curl -X PATCH \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"description":"Updated description"}' \
     https://api.github.com/repos/owner/repo

删除仓库：

.. code-block:: bash

   curl -X DELETE \
     -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/repos/owner/repo

**Issue 操作**

获取 Issue 列表：

.. code-block:: bash

   curl https://api.github.com/repos/owner/repo/issues

响应：

.. code-block:: json

   [
     {
       "number": 1,
       "title": "Bug report",
       "state": "open",
       "body": "Description",
       "user": {
         "login": "username"
       },
       "labels": [
         {"name": "bug"}
       ]
     }
   ]

创建 Issue：

.. code-block:: bash

   curl -X POST \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"title":"Bug report","body":"Description","labels":["bug"]}' \
     https://api.github.com/repos/owner/repo/issues

更新 Issue：

.. code-block:: bash

   curl -X PATCH \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"state":"closed"}' \
     https://api.github.com/repos/owner/repo/issues/1

**PR 操作**

获取 PR 列表：

.. code-block:: bash

   curl https://api.github.com/repos/owner/repo/pulls

创建 PR：

.. code-block:: bash

   curl -X POST \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"title":"Fix bug","head":"feature-branch","base":"main","body":"Description"}' \
     https://api.github.com/repos/owner/repo/pulls

合并 PR：

.. code-block:: bash

   curl -X PUT \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"commit_title":"Merge pull request #1","merge_method":"merge"}' \
     https://api.github.com/repos/owner/repo/pulls/1/merge

**工作流操作**

获取工作流运行列表：

.. code-block:: bash

   curl https://api.github.com/repos/owner/repo/actions/runs

触发工作流：

.. code-block:: bash

   curl -X POST \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"ref":"main","inputs":{"environment":"production"}}' \
     https://api.github.com/repos/owner/repo/actions/workflows/workflow.yml/dispatches

Python 实战示例
---------------

用 Python 调用 REST API，完成自动化任务。

**安装依赖**

.. code-block:: bash

   pip install requests PyGithub

``requests`` 是 HTTP 库，``PyGithub`` 是 GitHub API 的 Python 少封装。

**示例：批量创建 Issue**

.. code-block:: python

   import requests
   
   # Token
   TOKEN = "YOUR_TOKEN"
   
   # API endpoint
   url = "https://api.github.com/repos/owner/repo/issues"
   
   headers = {
       "Authorization": f"token {TOKEN}",
       "Accept": "application/vnd.github.v3+json"
   }
   
   # Issue 数据
   issues = [
       {"title": "Bug 1", "body": "Description 1", "labels": ["bug"]},
       {"title": "Bug 2", "body": "Description 2", "labels": ["bug"]},
       {"title": "Feature 1", "body": "Description 3", "labels": ["enhancement"]}
   ]
   
   # 批量创建
   for issue in issues:
       response = requests.post(url, headers=headers, json=issue)
       if response.status_code == 201:
           print(f"Created issue #{response.json()['number']}: {issue['title']}")
       else:
           print(f"Failed to create issue: {response.json()['message']}")

**示例：获取仓库统计数据**

.. code-block:: python

   from github import Github
   
   # Token
   g = Github("YOUR_TOKEN")
   
   # 仓库
   repo = g.get_repo("owner/repo")
   
   # 统计数据
   print(f"Stars: {repo.stargazers_count}")
   print(f"Forks: {repo.forks_count}")
   print(f"Open Issues: {repo.open_issues_count}")
   print(f"Watchers: {repo.watchers_count}")
   
   # 获取最近 Issue
   issues = repo.get_issues(state="open", sort="created", direction="desc")
   for issue in issues[:5]:
       print(f"#{issue.number}: {issue.title}")

**示例：检查 PR 状态**

.. code-block:: python

   from github import Github
   
   g = Github("YOUR_TOKEN")
   repo = g.get_repo("owner/repo")
   
   # 获取待审查的 PR
   pulls = repo.get_pulls(state="open", sort="created", direction="desc")
   
   for pr in pulls:
       # 检查是否可以合并
       if pr.mergeable:
           print(f"#{pr.number}: {pr.title} - Ready to merge")
       else:
           print(f"#{pr.number}: {pr.title} - Conflicts")
       
       # 检查审查状态
       reviews = pr.get_reviews()
       approved = any(review.state == "APPROVED" for review in reviews)
       if approved:
           print(f"  ✓ Approved")
       else:
           print(f"  ⏳ Pending review")

GraphQL API 基础
----------------

GraphQL 是查询语言，一次请求获取多个资源。

**GraphQL Endpoint**

::

   https://api.github.com/graphql

所有 GraphQL 请求都发送到这个 URL（POST 方法）。

**查询示例**

获取仓库信息和最近 Issue：

.. code-block:: json

   {
     repository(owner: "owner", name: "repo") {
       name
       description
       stargazerCount
       issues(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
         totalCount
         nodes {
           number
           title
           state
           createdAt
         }
       }
     }
   }

响应：

.. code-block:: json

   {
     "data": {
       "repository": {
         "name": "repo",
         "description": "My repository",
         "stargazerCount": 123,
         "issues": {
           "totalCount": 100,
           "nodes": [
             {
               "number": 100,
               "title": "Recent issue",
               "state": "OPEN",
               "createdAt": "2024-01-15T10:00:00Z"
             }
           ]
         }
       }
     }
   }

**使用 GraphQL**

Python 示例：

.. code-block:: python

   import requests
   
   TOKEN = "YOUR_TOKEN"
   url = "https://api.github.com/graphql"
   
   headers = {
       "Authorization": f"bearer {TOKEN}",
       "Content-Type": "application/json"
   }
   
   query = """
   {
     repository(owner: "owner", name: "repo") {
       name
       issues(first: 10) {
         totalCount
       }
     }
   }
   """
   
   response = requests.post(url, headers=headers, json={"query": query})
   print(response.json())

**GraphQL vs REST**

REST API 获取仓库信息和 Issue 需要两次请求：

.. code-block:: bash

   GET /repos/owner/repo
   GET /repos/owner/repo/issues

GraphQL API 一次请求：

.. code-block:: json

   {
     repository(owner: "owner", name: "repo") {
       name
       issues(first: 10) {
         nodes {
           title
         }
       }
     }
   }

GraphQL 减少请求次数，适合复杂查询。

API 的最佳实践
--------------

**使用正确的认证方式**

- 个人使用：Personal Access Token（简单）
- 第三方应用：OAuth App（用户授权）
- 企业集成：GitHub App（安全、精细）

**处理速率限制**

检查剩余次数，避免超限：

.. code-block:: python

   response = requests.get(url, headers=headers)
   remaining = int(response.headers.get("X-RateLimit-Remaining"))
   
   if remaining < 100:
       # 速率接近限制，等待或使用缓存
       print(f"Rate limit approaching: {remaining} remaining")

**使用缓存**

重复请求相同资源，使用缓存减少 API 调用：

.. code-block:: python

   import time
   
   cache = {}
   cache_duration = 3600  # 1 小时
   
   def get_repo(owner, repo):
       key = f"{owner}/{repo}"
       if key in cache and time.time() - cache[key]["time"] < cache_duration:
           return cache[key]["data"]
       
       # API 调用
       response = requests.get(f"https://api.github.com/repos/{owner}/{repo}")
       cache[key] = {"data": response.json(), "time": time.time()}
       return cache[key]["data"]

**处理错误**

API 可能返回错误。检查状态码：

.. list-table:: HTTP 状态码
   :widths: 20 80
   :header-rows: 1

   * - 状态码
     - 说明
   * - 200
     - 成功
   * - 201
     - 创建成功
   * - 304
     - 未修改（使用缓存）
   * - 400
     - 错误请求（参数错误）
   * - 401
     - 未认证
   * - 403
     - 禁止访问（权限不足或速率限制）
   * - 404
     - 未找到
   * - 422
     - 验证失败

处理错误：

.. code-block:: python

   response = requests.post(url, headers=headers, json=data)
   
   if response.status_code == 201:
       print("Created successfully")
   elif response.status_code == 401:
       print("Authentication failed")
   elif response.status_code == 403:
       print("Access forbidden or rate limit exceeded")
   elif response.status_code == 422:
       print(f"Validation failed: {response.json()['message']}")
   else:
       print(f"Error: {response.status_code}")

**使用官方库**

GitHub 提供官方库，简化 API 调用：

- Python：PyGithub
- JavaScript：octokit
- Go：go-github
- Ruby：octokit.rb

使用官方库避免处理 HTTP 细节，专注业务逻辑。

从 API 到安全
-------------

API 让我们程序化访问 GitHub。但程序访问带来安全风险：Token 泄露、权限过大、未加密传输。

下一节我们会学习安全最佳实践——保护 Token、使用 Secrets、启用 Dependabot、安全扫描，确保 GitHub 使用安全。