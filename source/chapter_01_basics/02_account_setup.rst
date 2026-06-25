账户设置
========

创建 GitHub 账户是使用 GitHub 的第一步。

注册账户
--------

1. 访问 https://github.com
2. 点击 Sign up
3. 填写用户名、邮箱和密码
4. 验证邮箱地址

配置 SSH 密钥
-------------

使用 SSH 密钥可以避免每次推送代码时输入密码。

.. code-block:: bash

   # 生成 SSH 密钥
   ssh-keygen -t ed25519 -C "your_email@example.com"

   # 添加到 ssh-agent
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519

   # 将公钥添加到 GitHub
   cat ~/.ssh/id_ed25519.pub
   # 复制内容到 GitHub Settings > SSH and GPG keys