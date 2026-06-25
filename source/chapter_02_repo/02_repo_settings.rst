仓库设置
========

上一节我们创建了仓库。现在，让我们配置仓库设置——这些选项决定了仓库的安全性、协作方式和自动化程度。

打开仓库页面，点击 "Settings" 标签，你会看到众多配置选项。我们重点关注几个核心设置。

基本信息配置
------------

在 "General" 页面顶部，可以修改仓库的基本信息：

**仓库名称和描述**

创建后仍可修改名称。但要注意：改名后仓库 URL 会变化，其他人克隆的仓库需要更新远程地址：

.. code-block:: bash

   # 更新远程仓库地址
   git remote set-url origin https://github.com/yourname/new-name.git

描述建议定期更新，反映项目当前状态。

**网站链接**

如果你的项目有演示网站（如 GitHub Pages 或独立域名），可以填写 Homepage URL。访问者点击链接就能查看演示。

**主题标签（Topics）**

在仓库主页添加标签，如 ``python``, ``web-app``, ``machine-learning``。标签帮助 GitHub 分类仓库，用户搜索时更容易找到你的项目。

**可见性切换**

Public 和 Private 可以相互切换。但要注意：

- 从 Private 改为 Public：所有人可见历史提交，包括曾经的私有提交
- 从 Public 改为 Private：Fork 的仓库不会自动变为私有，仍公开可见

切换可见性前，建议检查提交历史是否有敏感信息。

分支保护：防止意外修改
-----------------------

分支保护是仓库最重要的安全设置。它防止重要分支（如 ``main``）被意外或恶意修改。

在 Settings → Branches 点击 "Add rule"，为 ``main`` 分支创建保护规则。

**核心保护选项**

.. list-table:: 分支保护规则详解
   :widths: 25 75
   :header-rows: 1

   * - 规则
     - 说明与作用
   * - Require a pull request before merging
     - 禁止直接推送到该分支，必须通过 PR 合并。防止个人随意修改主分支
   * - Require approvals
     - PR 合并前需要指定人数审核通过。确保代码质量，避免单人决策失误
   * - Require status checks to pass before merging
     - CI 测试通过后才能合并。防止未测试的代码进入主分支
   * - Require linear history
     - 禁止合并提交，只允许线性历史。保持提交历史清晰，便于回溯
   * - Do not allow bypassing the above settings
     - 即使是管理员也不能绕过规则。确保规则对所有人生效

**强制推送保护**

勾选 "Allow force pushes"（默认禁止）可以阻止 ``git push --force``。强制推送会覆盖远程历史，可能丢失其他人的提交。禁止这个操作能保护代码不丢失。

**删除保护**

勾选 "Allow deletions"（默认禁止）可以阻止分支删除。防止误删重要分支。

**为什么需要分支保护？**

一个真实案例：开发者凌晨修 Bug，直接推送到 ``main``，但修改有错误。第二天团队发现主分支代码损坏，回溯历史才发现是谁改的、改了什么。如果启用分支保护，修改必须通过 PR 和审核，错误在合并前就会被发现。

对于团队仓库，分支保护是必须的。对于个人仓库，如果只有你一个人开发，可以不启用。

协作者与团队管理
-----------------

在 Settings → Collaborators 可以添加协作者。

**添加协作者**

输入对方的 GitHub 用户名或邮箱，发送邀请。对方接受后，可以访问私有仓库，或推送代码到公开仓库。

**权限级别**

.. list-table:: 协作者权限级别
   :widths: 20 80
   :header-rows: 1

   * - 权限
     - 能做什么
   * - Read
     - 查看代码、克隆仓库、创建 Issue（最低权限）
   * - Triage
     - 管理 Issue 和 PR（添加标签、关闭 Issue），但不能推送代码
   * - Write
     - 推送代码、合并 PR（推荐给开发者）
   * - Maintain
     - 管理仓库设置、保护分支（推荐给项目维护者）
   * - Admin
     - 完全控制，包括删除仓库（最高权限）

根据协作者的角色分配合适权限，避免权限过大导致安全问题。

**团队管理**

如果你属于一个组织（Organization），可以在组织层面管理团队成员。组织的权限管理更灵活，可以创建团队、设置团队权限。

Webhooks：自动化触发器
-----------------------

Webhooks 让仓库事件触发外部服务。比如每次推送代码时，自动触发 CI 构建或通知 Slack。

在 Settings → Webhooks 点击 "Add webhook"：

- **Payload URL**：接收事件的服务地址
- **Content type**：数据格式（JSON 或 form）
- **Events**：触发事件类型（push、pull_request、issue 等）

常见应用场景：

- CI/CD 触发：推送代码后自动运行测试
- 通知集成：PR 创建时通知团队 Slack
- 自动部署：合并到 main 后自动部署服务器

GitHub Actions 提供了很多自动化功能，Webhooks 更适合与第三方服务集成。

其他重要设置
------------

**GitHub Pages**

在 Settings → Pages 可以配置静态网站托管。如果你的仓库有 ``index.html``，可以选择分支发布为网站。访问 ``yourname.github.io/repo-name`` 即可查看。

**Security**

Settings → Security 提供安全扫描选项：

- **Dependabot**：自动检测依赖漏洞，提交 PR 修复
- **CodeQL**：代码安全扫描，检测漏洞和错误
- **Secret scanning**：检测提交中的密钥泄露（如 API token）

建议启用这些功能，及时发现安全问题。

**Archiving**

项目结束维护时，可以在 Settings → General 底部选择 "Archive repository"。归档后仓库变为只读，不能再推送代码，但历史仍可查看。

配置建议总结
------------

不同阶段的仓库配置建议：

**个人仓库（初期）**

- 添加 README、.gitignore、LICENSE
- 启用 Dependabot 安全扫描
- 不启用分支保护（单人开发）

**团队仓库**

- 启用 main 分支保护
- 要求 PR 审核（至少 1 人）
- 要求 CI 检查通过
- 添加协作者，分配适当权限
- 配置 Webhooks 通知团队

**开源项目**

- 添加 CONTRIBUTING.md（贡献指南）
- 启用 Discussions（社区讨论）
- 启用所有安全扫描
- 创建 Issue 和 PR 模板

下一节我们深入分支管理——理解分支策略，让协作有条不紊。