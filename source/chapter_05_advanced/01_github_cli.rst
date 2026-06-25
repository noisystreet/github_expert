GitHub CLI
==========

GitHub CLI (gh) 是命令行工具，提高工作效率。

安装
----

.. code-block:: bash

   # macOS
   brew install gh

   # Linux
   sudo apt install gh

   # 验证安装
   gh --version

常用命令
--------

.. code-block:: bash

   # 认证
   gh auth login

   # 创建仓库
   gh repo create my-project

   # 创建 PR
   gh pr create --title "My PR" --body "Description"

   # 查看 PR
   gh pr list

   # 合并 PR
   gh pr merge 123