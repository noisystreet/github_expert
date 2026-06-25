Fork 与贡献
===========

上一节我们学习了团队管理——如何组织内部协作。现在的问题是：外部贡献者如何参与开源项目？

你不能把他们加为协作者（他们不属于你的团队）。你不能给他们推送权限（安全风险）。但他们想贡献代码，怎么实现？

Fork 工作流解决了这个问题。贡献者复制一份仓库到自己的账户，在自己的仓库上修改，然后请求原仓库合并改动。整个过程原仓库的控制权始终在你手中。

Fork 的本质
-----------

Fork 不是 Git 的概念，而是 GitHub 的功能。它复制一个仓库到你的账户，包括所有文件、分支和历史。但 Fork 与原仓库保持关联，可以同步原仓库的更新。

**Fork 与 Clone 的区别**

Clone 把仓库下载到本地，Fork 把仓库复制到你的 GitHub 账户。

- Clone：本地副本，与原仓库无关
- Fork：远程副本，与原仓库保持关联

Fork 后仍然需要 Clone，把 Fork 的仓库下载到本地才能修改。

**Fork 的用途**

Fork 主要用于两种场景：

1. **开源贡献**：向别人的项目贡献代码
2. **项目定制**：基于别人的项目做自己的版本

开源贡献是 Fork 的主要用途。据统计，GitHub 上每天有数万个 Fork，其中大部分是为了贡献代码。

Fork 工作流的完整流程
---------------------

假设你想向一个开源项目贡献代码。完整流程如下：

**第一步：Fork 原仓库**

打开原仓库页面，点击右上角的 "Fork" 按钮。GitHub 会复制一份仓库到你的账户。比如原仓库是 ``github.com/owner/project``，Fork 后变成 ``github.com/yourname/project``。

**第二步：Clone Fork 到本地**

.. code-block:: bash

   # Clone 你的 Fork
   git clone https://github.com/yourname/project.git
   cd project

现在你有了本地副本，可以修改代码。

**第三步：添加上游仓库**

你的 Fork 是从原仓库复制的，但不会自动同步原仓库的更新。需要添加上游仓库：

.. code-block:: bash

   # 添加原仓库为 upstream
   git remote add upstream https://github.com/owner/project.git

   # 查看远程仓库
   git remote -v
   # 输出：
   # origin    https://github.com/yourname/project.git (fetch)
   # origin    https://github.com/yourname/project.git (push)
   # upstream  https://github.com/owner/project.git (fetch)
   # upstream  https://github.com/owner/project.git (push)

 ``origin`` 指向你的 Fork，``upstream`` 指向原仓库。后续用 ``origin`` 推送你的改动，用 ``upstream`` 拉取原仓库的更新。

**第四步：创建功能分支**

不要在 main 分支上直接修改。创建一个功能分支：

.. code-block:: bash

   # 确保本地 main 与 upstream 同步
   git fetch upstream
   git checkout main
   git merge upstream/main

   # 创建功能分支
   git checkout -b feature/add-logging

这一步很重要：确保你的分支基于最新的 upstream/main。如果 upstream 有新提交，你的分支应该从最新版本分出，避免合并冲突。

**第五步：开发并提交**

在功能分支上修改代码：

.. code-block:: bash

   # 修改代码
   git add .
   git commit -m "Add logging feature"

   # 推送到你的 Fork
   git push origin feature/add-logging

推送后，你的 Fork 上就有了新分支 ``feature/add-logging``。

**第六步：创建 Pull Request**

打开你的 Fork 页面（``github.com/yourname/project``），GitHub 会提示 "feature/add-logging had recent pushes"。点击 "Compare & pull request"。

PR 页面会显示：

- **base repository**：原仓库（owner/project）
- **head repository**：你的 Fork（yourname/project）
- **base branch**：原仓库的 main 分支
- **head branch**：你的 feature/add-logging 分支

确认后点击 "Create pull request"。PR 就发送到原仓库了。

原仓库的维护者会审查你的改动，决定是否合并。

保持 Fork 同步
--------------

你的 Fork 不会自动同步原仓库的更新。原仓库可能有新提交，但你的 Fork 还是旧版本。定期同步是必要的。

**同步方法**

.. code-block:: bash

   # 拉取 upstream 的更新
   git fetch upstream

   # 切换到 main 分支
   git checkout main

   # 合并 upstream/main 到本地 main
   git merge upstream/main

   # 推送到你的 Fork
   git push origin main

这样你的 Fork 的 main 分支就与原仓库同步了。

**为什么需要同步？**

假设原仓库在你 Fork 后修复了一个 Bug。你的 Fork 没有这个修复。如果你基于旧版本开发，合并时可能冲突。

同步确保你的开发基于最新版本，减少冲突风险。

**同步频率**

建议在每次开发新功能前同步。或者每周同步一次，取决于原仓库的活跃度。

如果原仓库频繁更新（每天多个提交），建议每次开发前同步。如果原仓库很少更新，每周同步足够。

处理合并冲突
------------

创建 PR 后，原仓库可能有新提交与你的改动冲突。GitHub 会提示 "This branch has conflicts that must be resolved"。

**冲突的原因**

::

   时间线：
   ┌─────────────────────────────────────────────────┐
   │ Upstream main: A → B → C                        │
   │                   ↑                             │
   │                   Fork main (你 Fork 时的版本)   │
   │                   ↓                             │
   │ Your feature:    A → D (你的改动)               │
   │                                              │
   │ Upstream 新提交: B → C                         │
   │                                              │
   │ 合并时：C 和 D 都改了同一文件 → 冲突             │
   └─────────────────────────────────────────────────┘

原仓库在你 Fork 后有新提交 C。你的 Fork 从 A 分出，有提交 D。合并时 C 和 D 改了同一文件，冲突。

**解决方法**

在你的 Fork 上解决冲突：

.. code-block:: bash

   # 拉取 upstream 的更新
   git fetch upstream

   # 切换到功能分支
   git checkout feature/add-logging

   # 合并 upstream/main 到功能分支
   git merge upstream/main

   # 如果有冲突，手动解决
   # 编辑冲突文件，选择保留的内容

   # 提交解决后的文件
   git add .
   git commit -m "Resolve merge conflicts"

   # 推送到 Fork
   git push origin feature/add-logging

推送后，PR 自动更新，冲突状态变为已解决。

**预防冲突**

冲突无法完全避免，但可以减少：

- 开发前同步 upstream
- 开发时间尽量短，减少冲突窗口
- 改动范围尽量小，减少冲突面积
- 与维护者沟通，了解他们的开发计划

开源贡献的最佳实践
------------------

**阅读贡献指南**

开源项目通常有 ``CONTRIBUTING.md`` 文件，说明贡献规则：

- 代码风格要求
- 提交信息格式
- PR 审查流程
- 功能开发规范

阅读这份文件，避免违反规则。比如项目要求提交信息格式为 "feat: add feature"，如果你写 "add feature"，PR 可能被拒绝。

**从小改动开始**

第一次贡献建议选择小改动：

- 修复文档错别字
- 添加单元测试
- 修复小 Bug

这些改动风险低，容易审查，能快速通过。积累经验后再尝试大的改动。

很多开源项目有 "good first issue" 标签，标记适合新手的 Issue。从这里开始是个好选择。

**一个 PR 只做一件事**

PR 应该专注。如果一个 PR 包含功能添加、Bug 修复、重构，审查者难以理解每个改动。

拆分成多个 PR：

- PR 1：修复 Bug
- PR 2：添加功能
- PR 3：重构代码

这样每个 PR 目标明确，审查效率更高。

**清晰的 PR 描述**

PR 描述应该说明：

- 改动了什么
- 为什么改动
- 如何测试
- 相关 Issue（如 "Fixes #123"）

维护者可能不了解你的背景，清晰的描述能帮助他们理解改动意图。

**耐心等待审查**

维护者可能很忙，PR 可能需要几天甚至几周审查。不要催促，耐心等待。

如果 PR 长时间没有回应，可以礼貌地询问："Hi, is there anything I can do to help move this PR forward?"

**尊重审查意见**

维护者可能拒绝你的 PR，或要求修改。这是正常的，不要气馁。

- 如果意见合理，修改代码
- 如果意见不合理，礼貌地解释你的想法
- 如果最终拒绝，感谢维护者的时间，继续寻找其他贡献机会

开源贡献不仅是提交代码，更是学习和成长的过程。

Fork 的其他用途
---------------

除了开源贡献，Fork 还有其他用途：

**项目定制**

某个开源项目满足你的大部分需求，但有些细节不符合。你可以 Fork 它，修改成你想要的版本。

比如 Fork 一个博客模板，改造成你的个人博客。你拥有完全控制权，可以随意修改。

**项目保存**

某个项目可能被删除或变为私有。你可以 Fork 一份，保存代码。

但要注意：Fork 可能违反原作者的意愿。如果项目删除是因为法律问题，你的 Fork 也可能有问题。

**实验性开发**

想尝试一个新想法，但不想影响原仓库。Fork 一份，在 Fork 上实验。成功了再提交 PR，失败了就删除 Fork。

Fork 的管理
-----------

Fork 多了会难以管理。GitHub 提供了一些工具：

- **Your repositories**：查看你所有的仓库和 Fork
- **Forks**：原仓库页面可以查看所有 Fork
- **Delete**：不再需要的 Fork 可以删除

建议定期清理不需要的 Fork。删除 Fork 不影响原仓库，也不影响已合并的 PR。

从 Fork 到 Issue
----------------

Fork 是贡献代码的方式，但开源参与不止于此。Issue 是另一种参与方式：报告 Bug、提出建议、参与讨论。

下一节我们会深入 Issue 跟踪——如何创建有效的 Issue、如何管理 Issue、如何用 Issue 驱动项目进展。