安全最佳实践
============

前两节我们学习了 GitHub CLI 和 GitHub API——提高效率的自动化工具。但自动化带来安全风险：Token 泄露、密钥暴露、依赖漏洞。

安全不是可选的，而是必需的。一个安全漏洞可能导致：

- 代码被恶意修改
- 数据泄露
- 服务被攻击
- 品牌信誉受损

本节我们会学习 GitHub 的安全最佳实践：账户安全、代码安全、密钥管理、依赖安全、安全扫描。

账户安全
--------

账户是 GitHub 的入口。账户被盗，所有仓库都暴露。

**双因素认证（2FA）**

2FA 是账户安全的第一道防线。启用后，登录需要密码和验证码（手机或应用）。

启用 2FA：

1. GitHub 设置页面 → Password and authentication → Two-factor authentication
2. 选择方式：手机短信或认证应用（推荐）
3. 保存备用码（用于手机丢失时恢复）

认证应用推荐：

- Google Authenticator
- Authy
- 1Password
- Microsoft Authenticator

认证应用比手机短信更安全（短信可能被拦截）。

**强密码**

密码应该：

- 长度至少 12 位
- 包含大写、小写、数字、符号
- 不使用常见单词、生日、姓名
- 不与其他网站重复

使用密码管理器：

- 1Password
- LastPass
- Bitwarden

密码管理器自动生成强密码，无需记忆。

**检查授权应用**

第三方应用可能请求 GitHub 授权。定期检查授权应用，撤销不必要的授权。

检查授权应用：

1. GitHub 设置页面 → Applications → Authorized OAuth Apps
2. 查看列表，撤销不信任的应用

授权应用的风险：

- 应用可能读取私有仓库
- 应用可能写入代码
- Token 泄露后应用可操作你的账户

**检查安全日志**

GitHub 记录账户活动。检查日志可以发现异常登录。

查看日志：

1. GitHub 设置页面 → Security log
2. 查看登录、授权、密码修改等活动

异常迹象：

- 陌生 IP 地址登录
- 未知的授权应用
- 异常的仓库访问

发现异常立即修改密码、撤销授权、启用 2FA。

代码安全
--------

代码是项目的核心。代码安全问题影响用户和团队。

**密钥管理**

密钥（API Key、数据库密码、Token）不应硬编码在代码中。硬编码的密钥可能被推送到 GitHub，任何人可见。

错误做法：

.. code-block:: python

   # 错误：硬编码密钥
   API_KEY = "sk-1234567890abcdef"
   DB_PASSWORD = "password123"

正确做法：使用环境变量或 GitHub Secrets。

环境变量：

.. code-block:: python

   # 正确：从环境变量读取
   import os
   
   API_KEY = os.environ.get("API_KEY")
   DB_PASSWORD = os.environ.get("DB_PASSWORD")

GitHub Secrets：

GitHub Actions 可以使用 Secrets 存储密钥。Secrets 加密存储，不会在日志中显示。

添加 Secrets：

1. 仓库设置页面 → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 输入名称（如 ``API_KEY``）和值
4. Secrets 加密保存

使用 Secrets：

.. code-block:: yaml

   steps:
     - name: Use API
       run: python script.py
       env:
         API_KEY: ${{ secrets.API_KEY }}

Secrets 的限制：

- Secrets 最大 64KB
- Secrets 不能在日志中显示（GitHub 自动过滤）
- Secrets 只能在 Actions 中使用（不能在代码中直接读取）

**Secret Scanning**

GitHub 自动扫描代码中的密钥。发现泄露的密钥会通知你。

启用 Secret Scanning：

1. 仓库设置页面 → Security → Code security and analysis
2. 启用 "Secret scanning"

Secret Scanning 会检测：

- AWS Access Key
- GitHub Token
- Slack Token
- Google API Key
- 等数百种密钥

发现泄露会发送邮件通知，建议立即撤销密钥、修改代码。

**依赖安全**

项目依赖第三方库。第三方库可能有漏洞，影响项目安全。

依赖漏洞的风险：

- 被攻击者利用
- 数据泄露
- 服务中断

GitHub 提供多个工具检测依赖漏洞。

**Dependabot**

Dependabot 自动检测依赖漏洞，并创建 PR 修复。

启用 Dependabot：

1. 仓库设置页面 → Security → Code security and analysis
2. 启用 "Dependabot alerts"
3. 启用 "Dependabot security updates"

配置 Dependabot：

.. code-block:: yaml

   # .github/dependabot.yml
   version: 2
   updates:
     # Python 依赖
     - package-ecosystem: "pip"
       directory: "/"
       schedule:
         interval: "weekly"  # 每周检查
       open-pull-requests-limit: 5  # 最大 PR 数量
   
     # Node.js 依赖
     - package-ecosystem: "npm"
       directory: "/"
       schedule:
         interval: "daily"  # 每天检查

Dependabot 发现漏洞后会：

- 创建 Issue 报告漏洞
- 创建 PR 修复漏洞（自动更新依赖版本）
- 邀请你审查 PR

Dependabot 支持的生态系统：

- pip（Python）
- npm（Node.js）
- maven（Java）
- gradle（Java）
- cargo（Rust）
- go（Go）
- composer（PHP）

**依赖审查**

PR 中修改依赖时，GitHub 会显示依赖审查：

- 新依赖的安全等级
- 依赖的许可证
- 依赖的使用人数

依赖审查帮助你在合并前判断新依赖的安全性。

查看依赖审查：

PR 页面 → "Files changed" 标签 → 修改 ``requirements.txt`` 或 ``package.json`` 的文件 → 依赖审查提示。

安全扫描
--------

GitHub 提供多个安全扫描工具，检测代码漏洞。

**CodeQL**

CodeQL 是代码扫描工具，检测常见漏洞（SQL 注入、XSS、路径遍历等）。

启用 CodeQL：

1. 仓库设置页面 → Security → Code security and analysis
2. 启用 "CodeQL analysis"

或添加工作流：

.. code-block:: yaml

   # .github/workflows/codeql.yml
   name: CodeQL
   
   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]
   
   jobs:
     analyze:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout
           uses: actions/checkout@v4
   
         - name: Initialize CodeQL
           uses: github/codeql-action/init@v3
           with:
             languages: python
   
         - name: Perform CodeQL Analysis
           uses: github/codeql-action/analyze@v3

CodeQL 支持的语言：

- Python
- JavaScript/TypeScript
- Java
- C/C++
- Go
- Ruby

CodeQL 发现漏洞会：

- 创建 Security alert
- 标注漏洞位置
- 提供修复建议

**第三方扫描**

除了 CodeQL，GitHub 支持第三方扫描工具：

- SonarCloud
- Snyk
- Coverity
- Veracode

这些工具提供不同的扫描能力，可以集成到 GitHub Actions。

示例（SonarCloud）：

.. code-block:: yaml

   # .github/workflows/sonarcloud.yml
   name: SonarCloud
   
   on:
     push:
       branches: [main]
   
   jobs:
     sonarcloud:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: sonarsource/sonarcloud-github-action@master
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
             SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

**Security Advisory**

发现漏洞后，可以创建 Security Advisory，通知用户。

创建 Advisory：

1. 仓库 Security 页面 → "Security advisories"
2. 点击 "New security advisory"
3. 填写漏洞信息、影响范围、修复方案

Advisory 会：

- 发送邮件通知仓库 Star 用户
- 显示在仓库 Security 页面
- 可关联 CVE（Common Vulnerabilities and Exposures）

分支保护与安全
--------------

分支保护规则确保代码安全。

**分支保护规则**

保护重要分支（如 main、release）：

1. 仓库设置页面 → Branches → Branch protection rules
2. 点击 "Add rule"
3. 选择分支（如 main）
4. 配置规则

常用规则：

- **Require pull request before merging**：禁止直接推送，必须通过 PR
- **Require approvals**：PR 必须审查批准
- **Require status checks**：PR 必须通过 CI 测试
- **Require signed commits**：提交必须签名（防止伪造）
- **Restrict who can push**：限制推送权限（只有管理员可以）

这些规则防止：

- 未审查的代码合并
- 恶意提交
- CI 失败的代码

**签名提交**

Git 支持签名提交，证明提交来自你本人。

设置签名：

.. code-block:: bash

   # 生成 GPG 密钥
   gpg --full-generate-key
   
   # 查看密钥
   gpg --list-secret-keys --keyid-format LONG
   # 输出：sec   rsa4096/AB1234567890DEF
   
   # 导出公钥
   gpg --armor --export AB1234567890DEF
   
   # 添加到 GitHub：Settings → SSH and GPG keys → New GPG key

Git 配置签名：

.. code-block:: bash

   # 配置 Git 使用签名
   git config --global user.signingkey AB1234567890DEF
   git config --global commit.gpgsign true
   
   # 签名提交
   git commit -S -m "Signed commit"

GitHub 会显示 "Verified" 标签，证明提交已签名。

安全最佳实践总结
----------------

**账户安全**

- 启用 2FA（使用认证应用）
- 使用强密码（密码管理器）
- 定期检查授权应用
- 检查安全日志

**密钥管理**

- 不硬编码密钥（使用环境变量或 Secrets）
- 启用 Secret Scanning
- 定期轮换密钥

**依赖安全**

- 启用 Dependabot alerts
- 启用 Dependabot security updates
- 定期审查依赖

**代码扫描**

- 启用 CodeQL analysis
- 集成第三方扫描工具
- 创建 Security Advisory

**分支保护**

- 保护 main 分支
- 要求 PR、审查、CI
- 签名提交

安全是持续的过程，不是一次性配置。定期检查、更新、审查，确保项目安全。

从安全到自动化
----------------

本章我们学习了三个高级技巧：GitHub CLI 提高效率、GitHub API 程序化访问、安全最佳实践保障安全。

但 GitHub 的自动化能力不止于此。下一章我们会学习自动化工作流——使用 GitHub Actions 构建复杂的自动化流程：自动化测试、自动化部署、自动化发布、自动化通知，让 GitHub 成为自动化平台。