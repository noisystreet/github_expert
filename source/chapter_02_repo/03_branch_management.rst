分支管理
========

上一节我们配置了仓库的安全和协作设置。现在，让我们深入理解分支策略——这是团队协作的核心，决定了代码如何流动、如何集成。

为什么需要分支策略？假设一个团队有五个开发者，都在同一个分支上工作。开发者 A 改了登录模块，开发者 B 改了支付模块，两人同时推送代码。如果 A 的改动有 Bug，B 的支付模块也受影响，部署后用户无法支付。分支策略把不同功能的开发隔离到不同分支，避免互相干扰。

两种主流分支策略
-----------------

业界有两种主流分支策略：Git Flow 和 GitHub Flow。它们各有优劣，适合不同场景。

**Git Flow：完整的发布流程**

Git Flow 是 Vincent Driessen 在 2010 年提出的经典模型，适合有明确发布周期的项目：

::

   main ─────────────●─────────●──────────●  （生产环境）
                │         │         │
   release ─────●─────────●         │
                │                   │
   develop ─────●────●────●────●────●────●  （开发集成分支）
                │    │    │
   feature ─────●────●    │
                     │
   hotfix ───────────●───●

五种分支：

- ``main``：生产环境代码，只接受 release 或 hotfix 合并
- ``develop``：开发集成分支，feature 分支合并到这里
- ``feature/*``：功能分支，如 ``feature/login``，从 develop 分出
- ``release/*``：发布准备分支，如 ``release/v1.0``，测试和修复
- ``hotfix/*``：紧急修复分支，如 ``hotfix/login-error``，从 main 分出

**工作流程示例**

1. 从 ``develop`` 创建 ``feature/login`` 分支开发登录功能
2. 完成后合并回 ``develop``
3. 准备发布时，从 ``develop`` 创建 ``release/v1.0``
4. 在 ``release/v1.0`` 测试、修复 Bug（修复合并回 ``develop``）
5. 测试通过，合并 ``release/v1.0`` 到 ``main``，打标签 ``v1.0``
6. 生产环境发现紧急 Bug，从 ``main`` 创建 ``hotfix/login-error``
7. 修复后合并到 ``main`` 和 ``develop``

Git Flow 适合有计划发布周期的项目，比如每两周发布一个版本。但它复杂，五个分支类型让人困惑。小团队可能觉得繁琐。

**GitHub Flow：简化实用的模型**

GitHub Flow 是 GitHub 内部使用的简化模型，适合持续部署的项目：

::

   main ────●────●────●────●────●
            │         │
   feature  ●─────────●

只有 ``main`` 分支长期存在，其他分支都是临时的功能分支。

**工作流程**

1. ``main`` 分支的代码随时可部署
2. 开发新功能时，从 ``main`` 创建 ``feature/login``
3. 在 ``feature/login`` 开发、提交、推送
4. 创建 Pull Request，请求合并到 ``main``
5. 代码审查通过，CI 测试通过，合并
6. 合并后自动部署到生产环境

GitHub Flow 的核心假设：``main`` 分支随时可部署。这意味着每次合并前必须确保代码通过测试，可以上线。

**哪种策略适合你？**

.. list-table:: 分支策略选择
   :widths: 20 40 40
   :header-rows: 1

   * - 场景
     - 推荐
     - 原因
   * - 小团队、快速迭代
     - GitHub Flow
     - 简单，持续部署
   * - 大团队、计划发布
     - Git Flow
     - 有发布准备期，可测试
   * - 单人项目
     - GitHub Flow
     - 无需复杂分支

很多团队采用简化版本：保留 ``main`` 和 ``develop``，去掉 ``release`` 和 ``hotfix``。这比 Git Flow 简单，比 GitHub Flow 更有缓冲空间。

分支操作实战
-------------

理解策略后，让我们看看具体的分支操作。

**创建和切换分支**

.. code-block:: bash

   # 创建分支（但不切换）
   git branch feature/login

   # 切换到分支
   git checkout feature/login

   # 创建并切换（最常用）
   git checkout -b feature/login

   # 使用 switch 命令（Git 2.23+，更清晰）
   git switch -c feature/login

**查看分支**

.. code-block:: bash

   # 查看本地分支
   git branch
   # 输出：
   #   develop
   # * feature/login  （当前分支，* 标记）
   #   main

   # 查看所有分支（包括远程）
   git branch -a
   # 输出：
   #   develop
   # * feature/login
   #   main
   #   remotes/origin/develop
   #   remotes/origin/main

   # 查看分支最后一次提交
   git branch -v

**合并分支**

.. code-block:: bash

   # 切换到目标分支
   git checkout main

   # 合并 feature 分支
   git merge feature/login

   # 如果有冲突，解决后继续合并
   git add .
   git commit

合并有两种模式：

- **Fast-forward**：如果目标分支没有新提交，Git 直接移动指针，不产生合并提交
- **Three-way merge**：如果两个分支都有新提交，Git 创建一个合并提交

**删除分支**

.. code-block:: bash

   # 删除已合并的分支
   git branch -d feature/login

   # 强制删除未合并的分支（谨慎使用）
   git branch -D feature/login

   # 删除远程分支
   git push origin --delete feature/login

**推送分支**

.. code-block:: bash

   # 推送新分支到远程
   git push -u origin feature/login

   # 后续推送（已建立追踪）
   git push

 ``-u`` 参数建立追踪关系，后续 ``git pull`` 会自动从远程拉取，``git push`` 会自动推送到远程。

处理合并冲突
------------

合并分支时可能遇到冲突——两个分支修改了同一文件的同一部分。

冲突示例：

::

   <<<<<<< HEAD
   user = "Alice"
   =======
   user = "Bob"
   >>>>>>> feature/login

 ``<<<<<<< HEAD`` 到 ``=======`` 是当前分支的内容，``=======`` 到 ``>>>>>>> feature/login`` 是要合并的分支内容。

**解决步骤**

1. 打开冲突文件，理解冲突内容
2. 决定保留哪个版本，或合并两者
3. 删除冲突标记，编辑为正确内容
4. 添加并提交：

.. code-block:: bash

   git add file.txt
   git commit -m "Resolve merge conflict"

**预防冲突**

冲突不可避免，但可以减少：

- 频繁合并：不要让分支差异太大
- 小提交：每个提交改动少，冲突范围小
- 沟通协调：团队成员知道彼此改哪些文件

分支命名最佳实践
----------------

好的分支名称应该清晰表明用途：

**推荐命名格式**

- ``feature/short-description``：功能开发，如 ``feature/user-auth``
- ``bugfix/issue-number``：Bug 修复，如 ``bugfix/123-login-error``
- ``hotfix/issue-number``：紧急修复，如 ``hotfix/456-payment-fail``
- ``release/version``：发布准备，如 ``release/v1.2.0``
- ``experiment/name``：实验性开发，如 ``experiment/new-algorithm``

**命名原则**

- 使用前缀分类（feature、bugfix 等）
- 包含 Issue 编号便于追溯
- 描述简洁，用连字符分隔单词
- 避免过长（控制在 30 字符内）

从分支策略到工作流
------------------

分支管理只是开发流程的一部分。下一章我们会介绍 Pull Request 和代码审查——这是分支合并的关键环节，决定了代码如何从功能分支进入主分支。理解分支策略后，Pull Request 才有意义：它是在分支合并前设置的检查点，确保代码质量。