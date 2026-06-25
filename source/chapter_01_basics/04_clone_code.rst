克隆代码
========

上一节我们理解了仓库、分支和提交的概念。现在，让我们把这些概念付诸实践——克隆一个仓库到本地。

克隆（Clone）是将远程仓库完整复制到本地的操作。它不仅下载文件，还下载完整的提交历史、所有分支和配置信息。克隆后，你本地就拥有了仓库的全部内容，可以独立进行 Git 操作。

基本克隆操作
------------

找到你想克隆的仓库页面，点击绿色的 "Code" 按钮，你会看到克隆地址。选择 HTTPS 或 SSH 方式：

.. code-block:: bash

   # HTTPS 克隆（无需配置）
   git clone https://github.com/octocat/Hello-World.git

   # SSH 克隆（已配置密钥）
   git clone git@github.com:octocat/Hello-World.git

执行后，当前目录下会出现一个 ``Hello-World`` 文件夹，包含仓库的所有内容。进入目录查看：

.. code-block:: bash

   cd Hello-World

   # 查看仓库状态
   git status

   # 查看远程仓库信息
   git remote -v
   # 输出：
   # origin  https://github.com/octocat/Hello-World.git (fetch)
   # origin  https://github.com/octocat/Hello-World.git (push)

 ``origin`` 是 Git 给远程仓库起的默认别名。后续推送代码时，使用 ``git push origin main`` 就是推送到这个地址。

HTTPS vs SSH：如何选择
----------------------

两种克隆方式各有优劣，选择取决于你的环境。

**HTTPS 方式**

优点是零配置，只要能访问 GitHub 网站就能克隆。在公司网络中，SSH 端口（22）可能被防火墙封锁，HTTPS 端口（443）通常是开放的。

缺点是推送时需要认证。每次 ``git push`` 都要输入用户名和密码（或 token）。频繁推送时很繁琐。

.. code-block:: bash

   # 缓存密码减少输入（HTTPS 方式）
   git config --global credential.helper 'cache --timeout=3600'

这个配置缓存密码一小时，期间推送无需重复输入。

**SSH 方式**

优点是一次配置，永久免密推送。SSH 密钥认证比密码更安全，不会被暴力破解。

缺点是需要生成密钥并添加到 GitHub（上一节已详细介绍）。SSH 端口可能被防火墙封锁。

.. code-block:: bash

   # 推荐做法：日常开发用 SSH
   git clone git@github.com:user/repo.git

   # 应急做法：SSH 被封锁时用 HTTPS
   git clone https://github.com/user/repo.git

深度克隆：节省时间与空间
------------------------

有些仓库体积巨大。比如 Chromium 浏览器的仓库超过 20GB，完整克隆需要几小时。如果你只想查看最新代码，完整克隆浪费时间。

深度克隆（Shallow Clone）只获取最近的几次提交，不下载完整历史：

.. code-block:: bash

   # 只克隆最近一次提交
   git clone --depth 1 https://github.com/user/repo.git

   # 克隆最近 10 次提交
   git clone --depth 10 https://github.com/user/repo.git

 ``--depth 1`` 意味着只获取最新的一个提交。仓库体积可能从几 GB 缩减到几 MB。

**适用场景**

- CI/CD 构建：构建脚本只需要最新代码，完整历史无用
- 快速查看：只想浏览代码，不关心历史
- 网络受限：带宽有限，下载速度慢

**深度克隆的代价**

历史不完整，某些操作受限：

- 无法查看旧版本的代码
- ``git log`` 只能显示有限的提交
- 某些 Git 命令可能报错

如果后续需要完整历史，可以取消深度限制：

.. code-block:: bash

   git fetch --unshallow

单分支克隆：只获取需要的分支
-----------------------------

有些仓库有很多分支。比如 Linux 内核仓库有上千个分支，完整克隆会下载所有分支。如果你只需要 ``main`` 分支，下载其他分支浪费空间。

单分支克隆只获取指定分支：

.. code-block:: bash

   # 只克隆 main 分支
   git clone --single-branch --branch main https://github.com/user/repo.git

   # 只克隆某个 feature 分支
   git clone --single-branch --branch feature/login https://github.com/user/repo.git

 ``--single-branch`` 参数告诉 Git 只下载指定分支，不下载其他分支的历史。

稀疏克隆：只下载需要的目录
---------------------------

大型仓库可能有复杂的目录结构。比如一个 monorepo 仓库包含多个项目：

::

   monorepo/
   ├── project-a/
   ├── project-b/
   ├── project-c/
   └── docs/

如果你只负责 ``project-a``，下载其他项目浪费空间。稀疏克隆（Sparse Clone）只获取指定目录：

.. code-block:: bash

   # 初始化稀疏克隆
   git clone --filter=blob:none --sparse https://github.com/user/monorepo.git
   cd monorepo

   # 只获取 project-a 目录
   git sparse-checkout set project-a

   # 或获取多个目录
   git sparse-checkout set project-a docs

 ``--filter=blob:none`` 是一个高级参数，避免下载文件内容（blob），只下载目录结构。后续 ``sparse-checkout`` 只下载指定目录的文件内容。

这种克隆方式适合大型 monorepo，显著减少下载量和本地占用空间。

克隆后的第一步
--------------

克隆完成后，进入仓库目录，建议先了解仓库状态：

.. code-block:: bash

   cd repository

   # 查看分支列表
   git branch -a
   # 输出：
   # * main                （当前分支，* 标记）
   #   remotes/origin/main （远程分支）

   # 查看最近的提交历史
   git log --oneline -5
   # 输出：
   # a1b2c3d (HEAD -> main, origin/main) Update README
   # e4f5g6h Add new feature
   # ...

   # 查看远程仓库信息
   git remote -v

这些命令帮助你了解仓库的当前状态：有哪些分支、最近的改动、远程仓库地址。

如果仓库有 ``README.md``，建议先阅读它，了解项目的用途和结构。

从克隆到修改
------------

克隆只是第一步。接下来你可能：

- 切换到其他分支：``git checkout branch-name``
- 创建自己的分支：``git checkout -b feature/my-feature``
- 查看某个历史版本：``git checkout commit-hash``
- 修改代码并提交：``git add`` → ``git commit`` → ``git push``

下一章我们会深入讲解仓库的创建和管理，从被动克隆到主动创建，完整掌握 GitHub 的核心操作。