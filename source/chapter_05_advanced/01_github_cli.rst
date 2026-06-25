GitHub CLI
==========

前四章我们学习了 GitHub 的核心功能：仓库管理、工作流、协作开发。这些功能主要通过网页操作。但如果每次操作都要打开浏览器、点击按钮，效率很低。

GitHub CLI（命令行工具）让你在终端中完成 GitHub 操作：创建仓库、提交 PR、查看 Issue、触发工作流……无需离开终端，效率大幅提升。

GitHub CLI 的优势
-----------------

**效率提升**

网页操作需要多个步骤：

- 打开浏览器 → 登录 GitHub → 找到仓库 → 点击按钮 → 填写表单 → 提交

CLI 只需一个命令：

.. code-block:: bash

   gh pr create --title "Fix bug" --body "Description"

几秒钟完成，无需离开终端。

**脚本化**

CLI 命令可以在脚本中使用。比如批量创建 Issue、自动化发布流程、定期检查仓库状态。

网页操作无法脚本化，只能手动执行。

**与 Git 集成**

CLI 与 Git 命令无缝衔接。在 Git 工作流中穿插 GitHub 操作，无需切换工具：

.. code-block:: bash

   git checkout -b feature/new-feature
   git commit -m "Add feature"
   git push origin feature/new-feature
   gh pr create  # 直接创建 PR，无需打开浏览器

**跨平台**

CLI 支持 macOS、Linux、Windows、 FreeBSD。无论你用什么操作系统，都能使用。

安装与认证
----------

**安装**

macOS 使用 Homebrew：

.. code-block:: bash

   brew install gh

Linux（Debian/Ubuntu）：

.. code-block:: bash

   sudo apt update
   sudo apt install gh

Linux（Fedora/CentOS）：

.. code-block:: bash

   sudo dnf install gh

Windows 使用 winget：

.. code-block:: bash

   winget install --id GitHub.cli

或下载安装包：https://github.com/cli/cli/releases/latest

验证安装：

.. code-block:: bash

   gh --version
   # 输出：gh version 2.40.0 (2024-01-15)

**认证**

安装后需要认证 GitHub 账户：

.. code-block:: bash

   gh auth login

CLI 会询问：

1. **GitHub 财户类型**：GitHub.com 或 GitHub Enterprise
2. **认证方式**：HTTPS 或 SSH
3. **登录方式**：浏览器或 Token

推荐选择浏览器登录，CLI 会打开浏览器，你登录 GitHub 后自动完成认证。

认证成功后：

.. code-block:: bash

   gh auth status
   # 输出：
   # ✓ Logged in to github.com as your-username
   # ✓ Git operations configured for HTTPS

**管理认证**

切换账户：

.. code-block:: bash

   gh auth switch

退出认证：

.. code-block:: bash

   gh auth logout

仓库操作
--------

**创建仓库**

从本地项目创建 GitHub 仓库：

.. code-block:: bash

   # 在项目目录执行
   gh repo create my-project --public

CLI 会：

- 在 GitHub 创建仓库
- 添加 Git remote（origin）
- 掐送本地代码到 GitHub

其他选项：

.. code-block:: bash

   gh repo create my-project --private  # 私有仓库
   gh repo create my-project --description "My project"  # 添加描述
   gh repo create my-project --template owner/template-repo  # 使用模板
   gh repo create my-project --clone  # 克隆到本地

**克隆仓库**

克隆他人仓库：

.. code-block:: bash

   gh repo clone owner/repo-name

省略 owner 时克隆自己账户的仓库：

.. code-block:: bash

   gh repo clone repo-name

**查看仓库信息**

.. code-block:: bash

   gh repo view owner/repo-name

输出：

::

   owner/repo-name
   My Project
   
   This is my project description.
   
   License: MIT
   
   Stars: 123
   Forks: 45
   Issues: 10
   Watchers: 5
   
   Homepage: https://owner.github.io/repo-name

**删除仓库**

.. code-block:: bash

   gh repo delete owner/repo-name

CLI 会要求确认，防止误删。

PR 操作
-------

PR（Pull Request）是 GitHub 协作的核心。CLI 让 PR 操作更高效。

**创建 PR**

推送分支后直接创建 PR：

.. code-block:: bash

   gh pr create

CLI 会询问：

- PR 标题
- PR 正文
- Base 分支（默认当前仓库的默认分支）
- Reviewer（可选）

或直接指定：

.. code-block:: bash

   gh pr create --title "Fix login bug" --body "Description" --base main --head feature/login-fix

**从 Issue 创建 PR**

Issue 可以直接转为 PR：

.. code-block:: bash

   gh pr create --fill

``--fill`` 会从当前分支名推断 PR 标题和正文。如果分支名是 ``fix-login-bug-123``，PR 标题会是 "Fix login bug"，并关联 Issue #123。

**查看 PR**

列出 PR：

.. code-block:: bash

   gh pr list
   # 输出：
   # #123  Fix login bug  feature/login-fix  OPEN
   # #124  Add feature    feature/new-feat   OPEN

过滤 PR：

.. code-block:: bash

   gh pr list --state merged  # 已合并
   gh pr list --author your-username  # 作者过滤
   gh pr list --label bug  # 标签过滤
   gh pr list --limit 10  # 限制数量

查看 PR 详情：

.. code-block:: bash

   gh pr view 123

输出：

::

   #123 Fix login bug
   
   Status: OPEN
   Author: your-username
   Branch: feature/login-fix -> main
   Labels: bug
   
   Description:
   This PR fixes the login bug when password contains special characters.
   
   Changes:
   - Fix password validation
   
   Reviewers: reviewer-username

在浏览器中查看：

.. code-block:: bash

   gh pr view 123 --web

**审查 PR**

查看 PR 改动：

.. code-block:: bash

   gh pr diff 123

批准 PR：

.. code-block:: bash

   gh pr review 123 --approve --body "Looks good to me"

请求修改：

.. code-block:: bash

   gh pr review 123 --request-changes --body "Please fix the test"

评论：

.. code-block:: bash

   gh pr review 123 --comment --body "I have a question about..."

**合并 PR**

.. code-block:: bash

   gh pr merge 123

CLI 会询问合并方式：

- Merge commit
- Squash and merge
- Rebase and merge

或直接指定：

.. code-block:: bash

   gh pr merge 123 --merge  # Merge commit
   gh pr merge 123 --squash  # Squash
   gh pr merge 123 --rebase  # Rebase

**关闭 PR**

.. code-block:: bash

   gh pr close 123

Issue 操作
----------

**创建 Issue**

.. code-block:: bash

   gh issue create --title "Bug: Login fails" --body "Description"

或使用交互式输入：

.. code-block:: bash

   gh issue create

CLI 会询问标题、正文、标签、分配人。

**查看 Issue**

.. code-block:: bash

   gh issue list
   # 输出：
   # #10  Bug: Login fails  bug  OPEN
   # #11  Feature request   enhancement  OPEN

过滤 Issue：

.. code-block:: bash

   gh issue list --state closed  # 已关闭
   gh issue list --author your-username  # 作者过滤
   gh issue list --label bug  # 标签过滤
   gh issue list --assignee your-username  # 分配人过滤

查看 Issue 详情：

.. code-block:: bash

   gh issue view 10

**关闭 Issue**

.. code-block:: bash

   gh issue close 10

** reopened Issue**

.. code-block:: bash

   gh issue reopen 10

工作流操作
----------

GitHub Actions 工作流也可以用 CLI 管理。

**查看工作流**

.. code-block:: bash

   gh run list
   # 输出：
   # #123  CI  completed  success  main  2024-01-15
   # #124  CI  completed  failure  main  2024-01-14

查看运行详情：

.. code-block:: bash

   gh run view 123

实时查看运行日志：

.. code-block:: bash

   gh run watch 123

**触发工作流**

手动触发工作流：

.. code-block:: bash

   gh workflow run workflow-name

或指定工作流文件：

.. code-block:: bash

   gh workflow run ci.yml --ref main

传递参数：

.. code-block:: bash

   gh workflow run deploy.yml -f environment=production

**下载工作流产物**

工作流运行后可能生成产物（如构建文件、测试报告）：

.. code-block:: bash

   gh run download 123

下载到当前目录。或指定目录：

.. code-block:: bash

   gh run download 123 -D artifacts

Release 操作
------------

**创建 Release**

.. code-block:: bash

   gh release create v1.0.0 --title "Version 1.0" --notes "Release notes"

上传产物：

.. code-block:: bash

   gh release create v1.0.0 --title "Version 1.0" ./dist/app.zip

**查看 Release**

.. code-block:: bash

   gh release list
   # 输出：
   # v1.0.0  Version 1.0  2024-01-15
   # v0.9.0  Beta release  2024-01-01

查看详情：

.. code-block:: bash

   gh release view v1.0.0

下载 Release 产物：

.. code-block:: bash

   gh release download v1.0.0

**删除 Release**

.. code-block:: bash

   gh release delete v1.0.0

高级用法
--------

**别名**

常用命令可以设置别名：

.. code-block:: bash

   gh alias set prc "pr create"
   gh alias set prl "pr list"
   gh alias set prv "pr view"

现在可以用简短命令：

.. code-block:: bash

   gh prc --title "Fix bug" --body "Description"
   gh prl
   gh prv 123

查看别名：

.. code-block:: bash

   gh alias list

删除别名：

.. code-block:: bash

   gh alias delete prc

**扩展**

CLI 支持扩展，第三方工具可以添加命令：

.. code-block:: bash

   gh extension install owner/gh-extension-name

常用扩展：

- ``gh-dash``：终端中的 PR/Issue 看板
- ``gh-cache``：管理 GitHub Actions 缓存
- ``gh-preview``：预览 Markdown 文件

**脚本化**

CLI 命令可以在脚本中使用：

.. code-block:: bash

   # Bash script: create_issues.sh
   #!/bin/bash
   
   # 批量创建 Issue
   for i in {1..10}; do
     gh issue create --title "Task $i" --body "Description for task $i"
   done

或用于 CI/CD：

.. code-block:: yaml

   # GitHub Actions workflow
   name: Auto Release
   
   on:
     push:
       tags:
         - 'v*'
   
   jobs:
     release:
       runs-on: ubuntu-latest
       steps:
         - name: Create Release
           run: gh release create ${{ github.ref_name }} --title "Release ${{ github.ref_name }}"
           env:
             GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

**输出格式**

CLI 输出可以格式化：

.. code-block:: bash

   gh pr list --json title,state,author
   # 输出 JSON：
   # [{"title":"Fix bug","state":"OPEN","author":{"login":"user"}}]

   gh pr list --csv
   # 输出 CSV：
   # number,title,state,author
   # 123,Fix bug,OPEN,user

用 jq 处理 JSON 输出：

.. code-block:: bash

   gh pr list --json title,state --jq '.[] | select(.state == "OPEN") | .title'

从 CLI 到 API
-------------

CLI 覆盖了大部分 GitHub 操作。但对于更复杂的场景，需要使用 GitHub API。

CLI 本质上是 API 的命令行封装。理解 API 能让你：

- 编写程序自动化 GitHub 操作
- 开发 GitHub Apps
- 集成 GitHub 到自己的工具

下一节我们会深入学习 GitHub API——REST API、GraphQL API、认证与授权、速率限制。