Fork 与贡献
===========

Fork 是参与开源项目的主要方式。

Fork 工作流
-----------

.. code-block:: bash

   # 1. Fork 项目到自己的账户

   # 2. 克隆 Fork
   git clone https://github.com/your-username/project.git

   # 3. 添加上游仓库
   git remote add upstream https://github.com/original/project.git

   # 4. 创建功能分支
   git checkout -b feature/contribution

   # 5. 提交修改
   git commit -m "Add contribution"

   # 6. 推送到 Fork
   git push origin feature/contribution

   # 7. 创建 Pull Request

保持 Fork 同步
--------------

.. code-block:: bash

   git fetch upstream
   git checkout main
   git merge upstream/main