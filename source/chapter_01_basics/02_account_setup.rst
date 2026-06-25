账户设置
========

上一节我们了解了 GitHub 的定位——Git 的云端延伸，协作的社交平台。现在，让我们从实际操作开始：注册账户并配置开发环境。

注册 GitHub 账户
----------------

打开 https://github.com，你会看到注册页面。填写用户名、邮箱和密码，验证邮箱地址后，账户就创建完成了。

选择用户名时需要考虑几点：

- **简洁易记**：用户名会出现在你的个人主页 URL 中（``github.com/yourname``）
- **专业性**：如果你用于求职或开源贡献，建议使用真实姓名或常用昵称
- **一致性**：与其他平台（Twitter、LinkedIn）保持一致，便于识别

邮箱地址也很重要。GitHub 用邮箱识别提交者身份。如果你本地 Git 配置的邮箱与 GitHub 账户邮箱一致，提交记录会自动关联到你的账户。

.. code-block:: bash

   # 查看本地 Git 配置的邮箱
   git config --global user.email

   # 设置邮箱（与 GitHub 账户邮箱一致）
   git config --global user.email "your_email@example.com"

这段配置确保你的提交在 GitHub 上正确显示为你的贡献。

配置 SSH 密钥
-------------

注册完成后，第一个重要配置是 SSH 密钥。为什么需要它？

当你克隆或推送代码时，GitHub 要要验证你的身份。默认方式是 HTTPS，每次推送都要输入用户名和密码。如果你一天推送十次，就要输入十次密码，非常繁琐。

SSH 密钥解决了这个问题。配置完成后，GitHub 通过密钥识别你的身份，无需每次输入密码。这就像门锁配了一把专用钥匙，只要钥匙匹配就能进门，不用每次出示身份证。

**生成 SSH 密钥**

.. code-block:: bash

   # 生成 SSH 密钥（推荐使用 ed25519 算法）
   ssh-keygen -t ed25519 -C "your_email@example.com"

   # 查看公钥内容
   cat ~/.ssh/id_ed25519.pub

执行 ``ssh-keygen`` 时会问你几个问题：

- 文件保存位置：默认 ``~/.ssh/id_ed25519``，直接回车即可
- 密码保护：可选，设置后每次使用密钥需输入密码

公钥文件名以 ``.pub`` 结尾，私钥没有后缀。公钥要添加到 GitHub，私钥留在本地，**绝对不要泄露私钥**。

**添加公钥到 GitHub**

1. 复制公钥内容（上一条命令的输出）
2. 打开 GitHub Settings → SSH and GPG keys
3. 点击 "New SSH key"
4. 粘贴公钥内容，保存

**验证 SSH 连接**

.. code-block:: bash

   # 测试 SSH 连接
   ssh -T git@github.com

   # 成功输出示例：
   # Hi username! You've successfully authenticated, but GitHub does not provide shell access.

看到这条消息说明配置成功。以后推送代码时，GitHub 会自动识别你的身份。

HTTPS vs SSH：什么时候用哪种
-----------------------------

两种克隆方式各有适用场景：

.. list-table:: 克隆方式对比
   :widths: 20 40 40
   :header-rows: 1

   * - 方式
     - 适用场景
     - 注意事项
   * - HTTPS
     - 临时访问、防火墙严格环境
     - 可用 credential helper 缓存密码
   * - SSH
     - 日常开发、频繁推送
     - 需要配置密钥

在公司网络中，SSH 端口可能被封锁。这时只能用 HTTPS。GitHub 提供了 credential helper 缓存密码，减少输入频率：

.. code-block:: bash

   # 缓存密码 1 小时
   git config --global credential.helper 'cache --timeout=3600'

   # 或使用 Git Credential Manager（更安全）
   # Windows/macOS 可下载安装

对于日常开发，SSH 是更好的选择。配置一次，之后所有推送都免密，效率更高。

双因素认证（2FA）
-----------------

账户安全不容忽视。GitHub 支持双因素认证（Two-Factor Authentication），建议开启。

开启 2FA 后，登录时除了密码，还要输入动态验证码。验证码由手机应用（如 Google Authenticator）生成，每 30 秒变化一次。即使密码被盗，没有验证码也无法登录。

**设置步骤：**

1. Settings → Password and authentication
2. Enable two-factor authentication
3. 选择 "Security key"（硬件密钥）或 "TOTP"（手机应用）
4. 保存恢复码，用于手机丢失时恢复账户

开启 2FA 后，HTTPS 方式推送代码会受影响。密码不再有效，需要创建 Personal Access Token（PAT）替代密码：

1. Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. 选择权限范围（repo 权限即可）
4. 复制 token，推送时用它代替密码

.. code-block:: bash

   # HTTPS 推送时使用 token
   git push
   Username: your_username
   Password: ghp_xxxxxxxx（你的 token）

SSH 方式不受 2FA 影响，密钥认证仍然有效。这也是推荐 SSH 的一个原因。

个性化配置
----------

GitHub 提供了一些个性化选项，让你的账户更具辨识度：

**个人主页（Profile）**

- 添加头像：建议使用清晰的专业照片或标识性图标
- 编写简介：一句话介绍你的领域或兴趣
- 添加位置和网站链接

**README 展示**

创建一个与你用户名相同的仓库，添加 ``README.md``，内容会显示在个人主页上。很多开发者用它展示技术栈、项目列表或联系方式。

**邮件通知**

Settings → Notifications 控制邮件通知频率。建议：

- 开启 "Participating"：与你相关的讨论会通知
- 关闭 "Watching"：避免所有仓库的通知轰炸
- 开启 "Security"：安全警报必须接收

配置小结
--------

完成这些配置后，你的开发环境已准备就绪：

.. code-block:: bash

   # 确认配置状态
   git config --global user.name        # 用户名
   git config --global user.email       # 邮箱
   ssh -T git@github.com                # SSH 连接

三个命令都正常输出，说明配置成功。下一节我们会深入了解 GitHub 的核心概念——仓库、分支和提交，为实际操作打下基础。