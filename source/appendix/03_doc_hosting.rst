文档托管与发布
==============

本教程使用 Sphinx 构建，生成的 HTML 可以托管在多个平台。本章介绍常用的文档托管方式：GitHub Pages 和 ReadTheDocs。

GitHub Pages
------------

GitHub Pages 是 GitHub 提供的免费静态网站托管服务。适合个人博客、项目文档、展示页面。

**启用 GitHub Pages**

方式一：从分支部署

1. 仓库设置页面 → Pages → Source → Deploy from a branch
2. 选择分支（如 master）和目录（如 /docs 或 /）
3. GitHub 自动构建，生成 URL：``https://username.github.io/repo-name``

方式二：使用 GitHub Actions

第六章介绍了使用 GitHub Actions 自动部署 Sphinx 文档到 GitHub Pages：

.. code-block:: yaml

   name: Deploy Documentation
   
   on:
     push:
       branches: [master]
   
   permissions:
     pages: write
     id-token: write
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Setup Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         
         - name: Install Sphinx
           run: pip install sphinx sphinx-rtd-theme
         
         - name: Build documentation
           run: make html
         
         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: build/html
     
     deploy:
       needs: build
       runs-on: ubuntu-latest
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - uses: actions/deploy-pages@v4
           id: deployment

每次推送代码，文档自动更新。

**GitHub Pages 的限制**

- 只支持静态文件
- 单个仓库最多 1 GB
- 每月流量限制 100 GB
- 构建时间限制 10 分钟

**GitHub Pages 的优势**

- 免费
- 与 GitHub 集成
- 自定义域名支持
- HTTPS 支持

ReadTheDocs
-----------

ReadTheDocs 是专业的文档托管平台，专为 Sphinx、MkDocs 等文档工具设计。

**ReadTheDocs 的优势**

相比 GitHub Pages，ReadTheDocs 提供：

- **自动构建**：从 GitHub 拉取代码，自动构建文档
- **版本管理**：支持多版本文档（如 stable、latest、特定版本）
- **搜索功能**：内置全文搜索
- **PDF 导出**：自动生成 PDF 版本
- **Analytics**：文档访问统计
- **评论系统**：支持文档评论

**连接 GitHub 到 ReadTheDocs**

步骤：

1. **注册 ReadTheDocs**

   访问 https://readthedocs.org，使用 GitHub 账户登录。

2. **导入项目**

   点击 "Import a Project"，选择 GitHub 仓库。ReadTheDocs 会扫描仓库，检测文档配置。

3. **配置项目**

   填写项目信息：

   - Name：项目名称（如 "github-expert"）
   - Repository URL：GitHub 仓库地址
   - Default branch：默认分支（如 master 或 main）
   - Documentation type：文档类型（如 Sphinx）

4. **配置 .readthedocs.yaml**

   在仓库根目录添加配置文件：

   .. code-block:: yaml

      # .readthedocs.yaml
      version: 2
      
      build:
        os: ubuntu-22.04
        tools:
          python: "3.11"
      
      sphinx:
        configuration: source/conf.py
      
      formats:
        - pdf
        - epub
      
      python:
        install:
          - requirements:
              file: requirements.txt

   配置说明：

   - ``version``：配置文件版本（固定为 2）
   - ``build.os``：构建操作系统
   - ``build.tools.python``：Python 版本
   - ``sphinx.configuration``：Sphinx 配置文件路径
   - ``formats``：导出格式（HTML、PDF、EPUB）
   - ``python.install``：依赖安装

5. **触发构建**

   推送代码到 GitHub，ReadTheDocs 自动拉取并构建。或手动触发：

   ReadTheDocs 项目页面 → Build version → Build

**版本管理**

ReadTheDocs 支持多版本文档：

- **latest**：最新版本（跟踪默认分支）
- **stable**：稳定版本（最新的 Release）
- **自定义版本**：基于 Git Tag（如 v1.0、v2.0）

配置版本：

ReadTheDocs 项目设置 → Versions → Activate versions

激活特定 Tag，用户可以查看不同版本的文档。

示例：

::

   版本列表：
   - latest（跟踪 master 分支）
   - stable（最新的 Release Tag）
   - v1.0（基于 Tag v1.0）
   - v2.0（基于 Tag v2.0）

用户切换版本，查看对应文档。

**自定义域名**

ReadTheDocs 支持自定义域名：

1. ReadTheDocs 项目设置 → Domain → Add domain
2. 输入域名（如 "docs.example.com"）
3. 在域名服务商配置 DNS（CNAME 到 ``readthedocs.io``）
4. ReadTheDocs 提供 HTTPS

**ReadTheDocs 主题**

ReadTheDocs 提供专用主题（sphinx-rtd-theme），适合文档展示：

.. code-block:: python

   # conf.py
   html_theme = 'sphinx_rtd_theme'

安装：

.. code-block:: bash

   pip install sphinx-rtd-theme

主题特点：

- 响应式设计
- 左侧导航栏
- 版本切换
- 搜索框
- 阅读进度条

GitHub Pages vs ReadTheDocs
----------------------------

**选择 GitHub Pages 的场景**

- 个人博客、简单文档
- 不需要版本管理
- 不需要搜索功能
- 希望完全控制构建过程
- 已有 GitHub Actions 自动化

**选择 ReadTheDocs 的场景**

- 开源项目文档
- 需要多版本支持
- 需要搜索、PDF、评论功能
- 希望专业文档展示
- 不想自己维护构建流程

**示例对比**

GitHub Pages：

::

   URL: https://username.github.io/repo-name
   构建: GitHub Actions
   版本: 单版本
   搜索: 无（或第三方工具）
   PDF: 无

ReadTheDocs：

::

   URL: https://repo-name.readthedocs.io
   构建: ReadTheDocs 自动
   版本: 多版本（latest、stable、v1.0）
   搜索: 内置全文搜索
   PDF: 自动生成

最佳实践
--------

**文档与代码同仓库**

将文档放在代码仓库的子目录（如 ``docs/`` 或 ``source/``）：

- 文档与代码同步更新
- PR 可以同时修改代码和文档
- 文档变更历史与代码一致

**使用 CI 验证文档**

在 PR 中验证文档构建：

.. code-block:: yaml

   name: Test Docs
   
   on:
     pull_request:
       branches: [master]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         
         - run: pip install sphinx sphinx-rtd-theme
         
         - run: make html

确保文档构建成功，避免推送后 ReadTheDocs 构建失败。

**文档版本与代码版本对应**

Release 时创建文档版本：

.. code-block:: bash

   git tag v1.0.0
   git push origin v1.0.0

ReadTheDocs 自动识别 Tag，创建 v1.0 版本文档。

**使用警告块**

使用 Sphinx 的警告块突出重要信息：

.. code-block:: rst

   .. warning::
      This feature is deprecated and will be removed in v2.0.

   .. note::
      This is a new feature introduced in v1.5.

**交叉引用**

使用 Sphinx 的交叉引用链接相关内容：

.. code-block:: rst

   See :doc:`chapter_01_basics/index` for introduction.
   
   Refer to :ref:`pull-request` for details.

交叉引用在版本切换时自动更新路径。

从文档托管到持续学习
---------------------

文档托管让教程可访问。但学习不止于阅读文档——实践、交流、贡献才是掌握的关键。

下一节我们会介绍学习资源——官方文档、教程、社区、工具，帮助你持续深入学习 GitHub。