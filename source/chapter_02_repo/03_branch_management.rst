分支管理
========

合理的分支策略是团队协作的基础。

Git Flow
--------

经典的分支模型：

- ``main``: 生产环境代码
- ``develop``: 开发分支
- ``feature/*``: 功能分支
- ``release/*``: 发布分支
- ``hotfix/*``: 热修复分支

GitHub Flow
-----------

简化的分支模型：

.. code-block:: text

   main ────●────●────●────●────●
            │         │
   feature  ●─────────●

分支操作
--------

.. code-block:: bash

   # 查看分支
   git branch -a

   # 删除分支
   git branch -d feature/old-feature

   # 推送分支
   git push origin feature/new-feature