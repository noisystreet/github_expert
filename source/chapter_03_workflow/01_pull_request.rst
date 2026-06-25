Pull Request
============

Pull Request (PR) 是 GitHub 协作的核心功能。

创建 PR
-------

.. code-block:: bash

   # 创建功能分支
   git checkout -b feature/my-feature

   # 做一些修改
   git add .
   git commit -m "Implement my feature"

   # 推送分支
   git push origin feature/my-feature

然后在 GitHub 上创建 Pull Request。

PR 模板
-------

使用 PR 模板可以规范代码审查流程。

PR 最佳实践
-----------

- 保持 PR 小而专注
- 编写清晰的描述
- 添加必要的测试
- 响应审查意见