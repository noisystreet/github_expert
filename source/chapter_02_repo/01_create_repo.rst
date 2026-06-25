创建仓库
========

上一章我们学会了克隆别人的仓库。现在，让我们创建自己的仓库——从被动获取到主动建设，这是掌握 GitHub 的关键一步。

创建仓库的场景有两种：从零开始创建新项目，或者把本地已有的项目推送到 GitHub。

.. seealso::
   **知名仓库案例**
   
   GitHub 上有一些标志性仓库，展示了不同类型的项目：
   
   - **torvalds/linux**：Linux 内核源码，全球最大的开源项目之一，超过 30,000 个贡献者
   - **microsoft/vscode**：Visual Studio Code，最受欢迎的代码编辑器，超过 160,000 个 Star
   - **tensorflow/tensorflow**：Google 的机器学习框架，超过 180,000 个 Star
   - **github/gitignore**：各种语言的 .gitignore 模板集合，超过 150,000 个 Star
   - **electron/electron**：跨平台桌面应用框架，Atom、VS Code 都基于它
   
   这些仓库展示了 GitHub 的多样性：从操作系统到开发工具，从机器学习到实用模板。你的仓库可能就是下一个热门项目！

两种方式略有不同，我们逐一介绍。

从网页创建仓库
--------------

打开 GitHub 主页，右上角有一个 "+" 按钮，点击选择 "New repository"。你会看到一个创建页面，需要填写几个信息：

**仓库名称（Repository name）**

这是仓库的唯一标识，也决定了 URL 地址。比如命名为 ``my-first-app``，仓库地址就是 ``github.com/yourname/my-first-app``。

命名建议：

- 使用简短、有意义的名字
- 避免特殊字符（只用字母、数字、连字符和下划线）
- 如果是个人项目，可以用 ``yourname.github.io`` 作为主页仓库

**描述（Description）**

可选，但建议填写。一句话介绍仓库用途，帮助访问者快速理解项目。比如 "A simple to-do app built with Python"。

**公开或私有（Public/Private）**

这个选择很重要：

- **Public**：所有人可见，适合开源项目、展示作品
- **Private**：只有你和协作者可见，适合商业项目、实验代码

私有仓库不会影响 GitHub 的免费额度——GitHub 现在允许免费创建无限私有仓库。如果不确定，可以先创建私有仓库，等成熟后再改为公开。

**初始化选项**

三个可选的初始化文件：

- **Add a README file**：强烈建议勾选。README.md 是仓库的说明书，介绍项目用途、使用方法
- **Add .gitignore**：根据项目类型选择。Git 用它忽略不需要追踪的文件（如编译产物、临时文件）
- **Choose a license**：添加开源许可证，明确代码的使用权限

点击 "Create repository" 后，仓库就创建完成了。如果勾选了 README，GitHub 会自动创建一个初始提交，仓库就有了一个起点。

从命令行推送本地项目
--------------------

另一种场景：你本地已经有一个项目，想推送到 GitHub。步骤略有不同。

**第一步：在 GitHub 创建空仓库**

在 GitHub 上创建仓库，但**不要勾选任何初始化选项**。这会创建一个空仓库，没有任何提交。

**第二步：初始化本地 Git 仓库**

.. code-block:: bash

   cd my-project

   # 初始化 Git 仓库
   git init

   # 添加所有文件到暂存区
   git add .

   # 创建第一个提交
   git commit -m "Initial commit"

 ``git init`` 在当前目录创建 ``.git`` 子目录，存储 Git 的所有信息。这个目录就是仓库的"数据库"，千万别手动删除。

**第三步：连接远程仓库并推送**

.. code-block:: bash

   # 添加远程仓库地址
   git remote add origin https://github.com/yourname/my-project.git

   # 推送代码到 GitHub
   git push -u origin main

 ``origin`` 是远程仓库的别名（约定俗成的名字）。``-u`` 参数建立追踪关系，后续推送只需 ``git push``，不用再写 ``origin main``。

**为什么不能勾选初始化选项？**

如果勾选了 README，GitHub 仓库会有一个初始提交。但你的本地仓库也有一个初始提交（刚才创建的）。两个仓库历史不一致，推送时会报错：

::

   ! [rejected] main -> main (fetch first)
   error: failed to push some refs to 'https://github.com/yourname/my-project.git'

解决方法是先拉取 GitHub 的提交，合并后再推送：

.. code-block:: bash

   git pull origin main --allow-unrelated-histories
   git push -u origin main

但这样会产生一个合并提交，历史不够清晰。更简单的方式是：创建空仓库，避免这个问题。

使用模板仓库快速起步
---------------------

有些项目结构是固定的：React 项目、Python 包、静态网站等。每次从头创建繁琐且容易遗漏文件。

模板仓库（Template Repository）解决这个问题。它像一个配方，基于它创建的仓库会复制所有文件和目录结构。

GitHub 上有很多官方模板：

- ``github/pages-template``：GitHub Pages 静态网站
- ``github/actions-template``：GitHub Actions 工作流示例

你也可以创建自己的模板。把常用的项目结构整理成一个仓库，在仓库设置中勾选 "Template repository"。

使用模板创建仓库：

1. 找到模板仓库页面
2. 点击 "Use this template"（不是 Fork）
3. 填写新仓库名称
4. 创建后，新仓库继承模板的所有文件和提交历史

Fork 和 Use Template 的区别：

- **Fork**：保持与原仓库的关联，可以提交 Pull Request 贡献代码
- **Use Template**：创建独立的仓库，与模板无关，适合启动新项目

创建后的第一件事
-----------------

仓库创建完成后，建议先完善几个关键文件：

**README.md**

这是仓库的门面，访问者首先看到的内容。一个好的 README 应该包含：

- 项目名称和简介
- 安装/使用方法
- 配置说明
- 许可证信息
- 贡献指南（如果是开源项目）

一个简单的 README 示例：

::

   # My First App

   A simple to-do application built with Python.

   ## Installation

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

   ## License

   MIT License

**.gitignore**

告诉 Git 忽略哪些文件。常见忽略项：

- 编译产物：``*.pyc``, ``dist/``, ``build/``
- 依赖目录：``node_modules/``, ``venv/``
- IDE 配置：``.vscode/``, ``.idea/``
- 系统文件：``.DS_Store``, ``Thumbs.db``
- 密钥文件：``.env``, ``credentials.json``

GitHub 提供了常用语言的 .gitignore 模板：https://github.com/github/gitignore

**LICENSE**

开源许可证明确代码的使用权限。常见选择：

- **MIT**：宽松，允许任意使用、修改和分发
- **Apache 2.0**：类似 MIT，但提供专利保护
- **GPL**：严格，要求衍生项目也开源

如果没有许可证，代码默认受版权保护，他人不能自由使用。开源项目务必添加许可证。

从本地到远程的完整流程
-----------------------

创建仓库只是起点。接下来的开发流程：

.. code-block:: bash

   # 克隆仓库到本地
   git clone https://github.com/yourname/my-project.git

   # 开发过程中
   git add .                              # 添加改动
   git commit -m "Add feature X"          # 提交改动
   git push                               # 推送到 GitHub

   # 从 GitHub 拉取更新
   git pull

这三个命令构成 Git 的核心循环：``add`` → ``commit`` → ``push``。下一节我们会深入仓库的配置选项，让仓库更安全、更易协作。