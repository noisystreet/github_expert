创建仓库
========

创建仓库是项目的起点。

网页创建
--------

1. 点击右上角的 "+" 按钮
2. 选择 "New repository"
3. 填写仓库名称和描述
4. 选择公开或私有
5. 初始化 README、.gitignore 或 license

命令行创建
----------

.. code-block:: bash

   # 创建本地仓库
   mkdir my-project
   cd my-project
   git init

   # 添加远程仓库
   git remote add origin https://github.com/user/my-project.git

   # 推送代码
   git push -u origin main

仓库模板
--------

使用模板仓库可以快速开始新项目。