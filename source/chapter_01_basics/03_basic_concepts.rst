基本概念
========

理解这些核心概念对于使用 GitHub 至关重要。

仓库（Repository）
------------------

仓库是存储项目代码的地方，包含文件、文件夹和版本历史。

分支（Branch）
-------------

分支是独立的工作线，用于开发新功能而不影响主代码。

.. code-block:: bash

   # 创建并切换分支
   git checkout -b feature/new-feature

   # 合并分支
   git checkout main
   git merge feature/new-feature

提交（Commit）
--------------

提交是保存代码变更的快照。

.. code-block:: bash

   git add .
   git commit -m "Add new feature"