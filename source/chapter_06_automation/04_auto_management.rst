自动化项目管理
==============

前三节我们学习了自动化测试、部署、发布——这些都是代码相关的自动化。但项目管理（Issue 管理、PR 审查、团队协作）也需要自动化。

手动管理项目繁琐且容易遗漏。自动化项目管理让日常任务自动完成，团队专注核心工作。

自动标签：根据文件变更自动分类
------------------------------

**问题场景**

PR 创建后，需要手动添加标签（如 frontend、backend、documentation）。维护者可能忘记添加，导致 Issue 分类混乱。

自动标签根据 PR 改动的文件自动添加标签，无需手动干预。

**配置自动标签**

使用 ``actions/labeler`` Action：

.. code-block:: yaml

   name: Auto Label
   
   on:
     pull_request:
       types: [opened]
   
   permissions:
     contents: read
     pull-requests: write
   
   jobs:
     label:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/labeler@v5
           with:
             configuration-path: .github/labeler.yml

工作流解析：

- **on: pull_request: types: [opened]**：PR 创建时触发
- **permissions**：授予读取代码和修改 PR 的权限
- **configuration-path**：标签配置文件路径

**标签配置文件**

配置文件定义文件路径与标签的映射：

.. code-block:: yaml

   # .github/labeler.yml
   documentation:
     - changed-files:
       - any-glob-to-any-file: ['docs/**', '*.md', 'README*']
   
   backend:
     - changed-files:
       - any-glob-to-any-file: ['src/backend/**', 'api/**']
   
   frontend:
     - changed-files:
       - any-glob-to-any-file: ['src/frontend/**', 'assets/**', 'styles/**']
   
   tests:
     - changed-files:
       - any-glob-to-any-file: ['test/**', 'tests/**', '*_test.py']
   
   configuration:
     - changed-files:
       - any-glob-to-any-file: ['.github/**', '*.yml', '*.yaml']

规则解析：

- ``documentation``：改动文档文件时添加
- ``backend``：改动后端代码时添加
- ``frontend``：改动前端代码时添加
- ``tests``：改动测试文件时添加
- ``configuration``：改动配置文件时添加

**效果**

PR 创建时，工作流自动运行：

- 检查改动文件
- 匹配标签规则
- 添加相应标签

示例：

::

   PR 改动文件：
   - src/frontend/components/Header.tsx
   - styles/main.css
   
   自动添加标签：frontend

维护者无需手动添加标签，分类自动完成。

自动分配 Reviewer：根据规则分配审查者
-------------------------------------

**问题场景**

PR 创建后，需要手动分配审查者（Reviewer）。维护者可能忘记分配，PR 长时间无人审查。

自动分配根据规则自动分配审查者，确保 PR 及时审查。

**配置自动分配**

使用 ``kentaro-m/auto-assign-action``：

.. code-block:: yaml

   name: Auto Assign Reviewers
   
   on:
     pull_request:
       types: [opened]
   
   jobs:
     assign:
       runs-on: ubuntu-latest
       steps:
         - uses: kentaro-m/auto-assign-action@v2
           with:
             configuration-path: .github/auto_assign.yml

**分配配置文件**

配置文件定义分配规则：

.. code-block:: yaml

   # .github/auto_assign.yml
   addReviewers: true
   addAssignees: false
   
   reviewers:
     - reviewer1
     - reviewer2
     - reviewer3
   
   numberOfReviewers: 2
   
   # 根据文件路径分配
   filterLabels:
     frontend:
       reviewers:
         - frontend-expert1
         - frontend-expert2
     backend:
       reviewers:
         - backend-expert1
         - backend-expert2
   
   skipKeywords:
     - WIP
     - DO NOT REVIEW

规则解析：

- ``addReviewers``：是否添加审查者
- ``reviewers``：默认审查者列表
- ``numberOfReviewers``：分配数量（随机选择）
- ``filterLabels``：根据标签分配特定审查者
- ``skipKeywords``：PR 标题包含这些关键词时不分配

**效果**

PR 创建时：

- 从默认列表随机选择 2 个审查者
- 如果有 ``frontend`` 标签，选择 frontend 专家
- 如果标题包含 "WIP"，跳过分配

示例：

::

   PR 标题：Fix frontend bug
   
   自动分配：
   - frontend-expert1
   - frontend-expert2

**更精细的分配**

根据 PR 改动的文件路径分配：

.. code-block:: yaml

   - uses: actions/github-script@v7
     with:
       script: |
         const changedFiles = await github.rest.pulls.listFiles({
           owner: context.repo.owner,
           repo: context.repo.repo,
           pull_number: context.issue.number
         });
         
         const reviewers = [];
         
         for (const file of changedFiles.data) {
           if (file.filename.startsWith('src/frontend/')) {
             reviewers.push('frontend-expert');
           }
           if (file.filename.startsWith('src/backend/')) {
             reviewers.push('backend-expert');
           }
         }
         
         if (reviewers.length > 0) {
           await github.rest.pulls.requestReviewers({
             owner: context.repo.owner,
             repo: context.repo.repo,
             pull_number: context.issue.number,
             reviewers: reviewers
           });
         }

这个脚本根据文件路径动态分配审查者。

自动关闭过期 Issue：保持 Issue 列表整洁
----------------------------------------

**问题场景**

项目可能有大量过期 Issue：

- 问题已解决但 Issue 未关闭
- 问题不再发生但 Issue 还在
- Issue 长时间无人响应

这些 Issue 占用列表，维护者难以识别真正的问题。

自动关闭过期 Issue 让列表保持整洁。

**配置自动关闭**

使用 ``actions/stale``：

.. code-block:: yaml

   name: Close Stale Issues
   
   on:
     schedule:
       - cron: '0 0 * * *'  # 每天 UTC 0 点运行
   
   permissions:
     issues: write
     pull-requests: write
   
   jobs:
     stale:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/stale@v9
           with:
             days-before-stale: 30  # 30 天无活动标记过期
             days-before-close: 7  # 标记后 7 天关闭
             stale-issue-message: 'This issue has been inactive for 30 days. If this issue is still relevant, please comment or remove the stale label.'
             close-issue-message: 'This issue was closed due to inactivity.'
             stale-pr-message: 'This PR has been inactive for 30 days.'
             close-pr-message: 'This PR was closed due to inactivity.'
             exempt-issue-labels: 'pinned,security'  # 排除的标签
             exempt-pr-labels: 'pinned'

工作流解析：

- **cron: '0 0 * * *'**：每天运行一次
- **days-before-stale**：无活动多少天标记过期
- **days-before-close**：标记后多少天关闭
- **stale-issue-message**：标记时添加的评论
- **close-issue-message**：关闭时添加的评论
- **exempt-issue-labels**：排除的标签（不会关闭）

**效果**

Issue 流程：

::

   Issue 无活动 30 天
   → 添加 "stale" 标签
   → 评论：This issue has been inactive...
   → 7 天后仍然无活动
   → 关闭 Issue
   → 评论：This issue was closed due to inactivity.

如果 Issue 被标记后有人评论，移除 "stale" 标签，不会关闭。

**排除重要 Issue**

某些 Issue 不应该关闭：

- ``pinned``：固定 Issue（长期讨论）
- ``security``：安全 Issue（高优先级）

这些 Issue 标记排除标签，不会被关闭。

欢迎评论机器人：鼓励新贡献者
-----------------------------

**问题场景**

开源项目收到新贡献者的 PR。新贡献者可能不熟悉流程，需要引导。

欢迎评论机器人为新贡献者添加欢迎评论，鼓励参与。

**配置欢迎评论**

使用 ``actions/github-script``：

.. code-block:: yaml

   name: Welcome New Contributors
   
   on:
     pull_request:
       types: [opened]
   
   jobs:
     welcome:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/github-script@v7
           with:
             script: |
               // 获取作者的所有 PR
               const pulls = await github.rest.pulls.list({
                 owner: context.repo.owner,
                 repo: context.repo.repo,
                 state: 'all',
                 author: context.payload.pull_request.user.login
               });
               
               // 如果这是第一个 PR
               if (pulls.data.length === 1) {
                 await github.rest.issues.createComment({
                   owner: context.repo.owner,
                   repo: context.repo.repo,
                   issue_number: context.issue.number,
                   body: `🎉 欢迎 @${context.payload.pull_request.user.login}！\n\n这是你的第一个 PR。感谢你的贡献！\n\n如果你有任何问题，可以在评论中提问。`
                 });
               }

脚本解析：

- 获取作者的所有 PR
- 如果只有一个 PR（第一次贡献）
- 添加欢迎评论

**效果**

::

   新贡献者创建 PR
   → 机器人评论：🎉 欢迎 @username！
   → 鼓励新贡献者，引导参与

欢迎评论让新贡献者感受到社区的友好，提高参与意愿。

自动化报告：生成项目统计
------------------------

**问题场景**

团队需要了解项目进展：每周新增多少 Issue、多少 PR、多少代码改动。手动统计耗时。

自动化报告定期生成统计，发送给团队。

**配置每周报告**

使用 ``actions/github-script``：

.. code-block:: yaml

   name: Weekly Report
   
   on:
     schedule:
       - cron: '0 9 * * 1'  # 每周一 UTC 9 点
   
   jobs:
     report:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/github-script@v7
           with:
             script: |
               const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
               
               // 获取一周内的 Issue
               const issues = await github.rest.issues.listForRepo({
                 owner: context.repo.owner,
                 repo: context.repo.repo,
                 state: 'all',
                 since: oneWeekAgo
               });
               
               // 获取一周内的 PR
               const pulls = await github.rest.pulls.list({
                 owner: context.repo.owner,
                 repo: context.repo.repo,
                 state: 'all'
               });
               
               const recentPRs = pulls.data.filter(pr => 
                 new Date(pr.created_at) > new Date(oneWeekAgo)
               );
               
               // 创建 Issue 报告
               await github.rest.issues.create({
                 owner: context.repo.owner,
                 repo: context.repo.repo,
                 title: `Weekly Report - Week of ${new Date().toDateString()}`,
                 body: `
               ## 📊 Weekly Report
               
               ### Issues
               - New issues: ${issues.data.filter(i => i.state === 'open').length}
               - Closed issues: ${issues.data.filter(i => i.state === 'closed').length}
               
               ### Pull Requests
               - New PRs: ${recentPRs.filter(pr => pr.state === 'open').length}
               - Merged PRs: ${recentPRs.filter(pr => pr.merged_at).length}
               
               ### Contributors
               - Active contributors: ${new Set(issues.data.map(i => i.user.login).concat(recentPRs.map(pr => pr.user.login))).size}
               `
               });

脚本解析：

- 获取一周内的 Issue 和 PR
- 计算统计数据
- 创建 Issue 报告

**效果**

::

   每周一
   → 机器人创建 Issue：Weekly Report - Week of Jan 15, 2024
   → 内容包含 Issue、PR、贡献者统计
   → 团队查看报告，了解进展

自动化报告让团队随时了解项目状态。

其他自动化任务
--------------

**自动合并 PR**

满足条件时自动合并：

.. code-block:: yaml

   - uses: hmarr/auto-merge-action@v3
     with:
       required-labels: 'ready-to-merge'
       forbidden-labels: 'do-not-merge'

PR 有 "ready-to-merge" 标签且无 "do-not-merge" 标签时自动合并。

**自动创建 Issue**

定期创建 Issue（如每周提醒）：

.. code-block:: yaml

   - uses: actions/github-script@v7
     with:
       script: |
         await github.rest.issues.create({
           owner: context.repo.owner,
           repo: context.repo.repo,
           title: 'Weekly reminder: Update dependencies',
           body: 'Please check and update dependencies this week.'
         });

**自动回复 Issue**

根据关键词自动回复：

.. code-block:: yaml

   - uses: actions/github-script@v7
     with:
       script: |
         const issue = context.payload.issue;
         
         if (issue.title.includes('bug')) {
           await github.rest.issues.createComment({
             owner: context.repo.owner,
             repo: context.repo.repo,
             issue_number: issue.number,
             body: 'Thank you for reporting this bug. We will investigate it soon.'
           });
         }

**自动锁定旧 Issue**

Issue 关闭后自动锁定，防止新评论：

.. code-block:: yaml

   - uses: dessant/lock-threads@v4
     with:
       issue-lock-inactive-days: '30'

Issue 关闭 30 天后自动锁定。

自动化项目管理的最佳实践
-------------------------

**保持自动化简单**

自动化规则应该简单、明确：

- 不要过度复杂（难以维护）
- 不要过度自动化（失去人工判断）
- 测试规则是否有效（避免误操作）

**提供人工干预**

自动化不应该完全替代人工：

- 自动分配审查者，但允许手动更改
- 自动关闭过期 Issue，但允许重新打开
- 自动添加标签，但允许手动修改

自动化是辅助，不是替代。

**监控自动化效果**

定期检查自动化是否有效：

- 检查自动添加的标签是否准确
- 检查自动分配的审查者是否合理
- 检查自动关闭的 Issue 是否应该关闭

如果自动化效果不佳，调整规则或禁用。

**避免过度通知**

自动化可能发送大量通知（评论、邮件）。过度通知会干扰团队：

- 限制评论频率
- 避免重复通知
- 允许用户关闭通知

总结
----

本章我们学习了自动化工作流的四个方面：

1. **GitHub Actions 高级用法**：矩阵构建、缓存优化、复合动作、可重用工作流、环境与密钥管理
2. **自动化部署**：GitHub Pages、Docker Registry、云服务、Self-hosted Runners
3. **自动化发布**：版本号管理、GitHub Release、包管理平台、CHANGELOG 生成
4. **自动化项目管理**：自动标签、自动分配、自动关闭过期 Issue、欢迎评论、自动化报告

自动化让 GitHub 成为强大的平台：测试、部署、发布、管理全自动完成。团队专注核心工作，效率大幅提升。

但自动化不是目的，而是手段。选择合适的自动化场景，保持简单，提供人工干预，才能真正提高效率。

全书总结
========

本教程从 GitHub 基础入门到高级自动化，覆盖了 GitHub 的核心功能：

- 第一章：GitHub 简介、账户设置、基础概念、克隆代码
- 第二章：仓库创建、仓库设置、分支管理
- 第三章：Pull Request、代码审查、CI/CD
- 第四章：团队管理、Fork 与贡献、Issue 跟踪
- 第五章：GitHub CLI、GitHub API、安全最佳实践
- 第六章：GitHub Actions 高级用法、自动化部署、自动化发布、自动化项目管理

每个章节遵循"浅入深出、夹叙夹议"的风格，既有概念解释，又有实操示例，帮助读者快速上手 GitHub。

希望本教程能帮助你掌握 GitHub，提高协作效率，参与开源社区，成为优秀的开发者。