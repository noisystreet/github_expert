自动化发布
==========

上一节我们学习了自动化部署——代码自动上线。但部署只是发布的一部分。完整的发布流程包括：

- 版本号管理
- 创建 GitHub Release
- 生成 CHANGELOG
- 发布到包管理平台（npm、PyPI）

这些步骤手动完成很繁琐。自动化发布让整个过程无需手动干预，每次发布标准化、可追溯。

版本号与发布策略
----------------

**语义化版本**

语义化版本（Semantic Versioning）是版本号的标准格式：

::

   MAJOR.MINOR.PATCH
   
   如：2.1.3
   - MAJOR（2）：重大版本，不兼容的 API 变化
   - MINOR（1）：次要版本，向后兼容的功能新增
   - PATCH（3）：补丁版本，向后兼容的 Bug 修复

示例：

- 1.0.0 → 1.0.1：修复 Bug（PATCH）
- 1.0.1 → 1.1.0：新增功能（MINOR）
- 1.1.0 → 2.0.0：破坏兼容性（MAJOR）

语义化版本让用户一眼了解版本变化：

- MAJOR 升级：可能需要修改代码
- MINOR 升级：可以安全升级，有新功能
- PATCH 升级：可以安全升级，修复 Bug

**发布策略**

发布频率和方式取决于项目类型：

- **持续发布**：每次代码合并自动发布（适合 Web 应用）
- **定期发布**：每周/每月发布一次（适合大型项目）
- **按需发布**：功能完成后发布（适合小型项目）

发布策略应该明确：

- 何时发布（触发条件）
- 发布什么（发布内容）
- 如何发布（发布流程）

自动创建 GitHub Release
-----------------------

GitHub Release 是项目的发布记录。每个 Release 包含：

- 版本号（如 v1.0.0）
- 发布说明（Release Notes）
- 发布产物（如安装包、源码压缩包）
- 标签（Git Tag）

**手动创建 Release 的流程**

::

   1. 更新版本号（修改文件）
   2. 提交代码
   3. 创建 Git Tag
   4. 推送 Tag 到 GitHub
   5. 在 GitHub 上创建 Release
   6. 上传发布产物
   7. 编写发布说明

这个过程至少需要 10 分钟。频繁发布时很繁琐。

**自动化 Release**

推送 Tag 时自动创建 Release：

.. code-block:: yaml

   name: Create Release
   
   on:
     push:
       tags:
         - 'v*'
   
   permissions:
     contents: write
   
   jobs:
     release:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Build artifacts
           run: |
             npm install
             npm run build
             zip -r dist.zip dist/
         
         - name: Create Release
           uses: softprops/action-gh-release@v1
           with:
             generate_release_notes: true
             files: dist.zip

工作流解析：

- **on: push: tags: ['v*']**：推送 v 开头的 Tag 时触发
- **Build artifacts**：构建发布产物
- **Create Release**：创建 Release，上传产物
- **generate_release_notes: true**：自动生成发布说明

**推送 Tag 创建 Release**

手动创建 Tag：

.. code-block:: bash

   git tag v1.0.0
   git push origin v1.0.0

推送 Tag 后，工作流自动运行，创建 Release。

或使用 npm version：

.. code-block:: bash

   npm version patch  # 自动创建 Tag v1.0.1
   git push --follow-tags

``--follow-tags`` 推送代码和相关 Tag。

**自动生成发布说明**

GitHub Release 需要发布说明（描述本次发布的改动）。手动编写耗时，容易遗漏。

GitHub 提供自动生成功能：

.. code-block:: yaml

   - name: Create Release
     uses: softprops/action-gh-release@v1
     with:
       generate_release_notes: true

GitHub 根据提交历史生成发布说明：

::

   ## What's Changed
   ### Bug Fixes
   * Fix login bug by @user in #123
   ### Features
   * Add dark mode by @user in #124
   ### Documentation
   * Update README by @user in #125
   
   **Full Changelog**: https://github.com/owner/repo/compare/v1.0.0...v1.0.1

自动生成节省时间，确保完整性。

发布到包管理平台
----------------

库（Library）项目需要发布到包管理平台：npm（Node.js）、PyPI（Python）、Maven（Java）、Crates.io（Rust）。

**发布到 PyPI**

Python 项目发布到 PyPI：

.. code-block:: yaml

   name: Publish to PyPI
   
   on:
     release:
       types: [published]
   
   permissions:
     id-token: write
   
   jobs:
     pypi:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         
         - name: Install build tools
           run: pip install build
         
         - name: Build package
           run: python -m build
         
         - name: Publish to PyPI
           uses: pypa/gh-action-pypi-publish@release/v1

工作流解析：

- **on: release: types: [published]**：Release 发布时触发
- **id-token: write**：授予 OIDC 权限（用于 PyPI 认证）
- **Build package**：构建 Python 包
- **Publish to PyPI**：发布到 PyPI

**配置 PyPI OIDC**

PyPI 支持 OIDC（OpenID Connect）认证，无需 API Token：

1. PyPI 项目设置 → Publishing → Add GitHub repo
2. 配置仓库名称和工作流名称
3. 发布时自动认证

OIDC 比 API Token 更安全：

- 无需存储 Token
- Token 短期有效
- 限制特定仓库

**发布到 npm**

Node.js 项目发布到 npm：

.. code-block:: yaml

   name: Publish to npm
   
   on:
     release:
       types: [published]
   
   jobs:
     npm:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - uses: actions/setup-node@v4
           with:
             node-version: '20'
             registry-url: 'https://registry.npmjs.org'
         
         - run: npm ci
         - run: npm publish
           env:
             NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

工作流解析：

- **registry-url**：指定 npm Registry
- **NODE_AUTH_TOKEN**：npm 认证 Token（存储在 Secrets）

**配置 npm Token**

1. npm 账户设置 → Access Tokens → Generate New Token
2. 选择 Classic Token（或 Granular Access Token）
3. 复制 Token
4. GitHub 仓库设置 → Secrets → New repository secret → 添加 ``NPM_TOKEN``

**发布到 GitHub Packages**

GitHub 提供包管理服务：

.. code-block:: yaml

   - uses: actions/setup-node@v4
     with:
       node-version: '20'
       registry-url: 'https://npm.pkg.github.com'
   
   - run: npm publish
     env:
       NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

GitHub Packages 的优势：

- 包与仓库关联，权限管理方便
- 私有仓库的包也是私有的
- 无需额外账户

自动生成 CHANGELOG
------------------

CHANGELOG 是项目的变更历史。每个版本记录改动内容。

**手动编写 CHANGELOG 的问题**

::

   ## [1.0.1] - 2024-01-15
   ### Bug Fixes
   - Fix login bug (#123)
   ### Features
   - Add dark mode (#124)
   
   ## [1.0.0] - 2024-01-01
   ### Features
   - Initial release

手动编写耗时，容易遗漏改动。

**自动生成 CHANGELOG**

使用工具自动生成：

.. code-block:: yaml

   - name: Generate CHANGELOG
     uses: orhanciss/changelog-generator@v1
     with:
       token: ${{ secrets.GITHUB_TOKEN }}
       file: CHANGELOG.md

工具根据 Git 提交历史生成 CHANGELOG。

或使用 ``github-changelog-generator``：

.. code-block:: yaml

   - name: Generate CHANGELOG
     run: |
       gem install github_changelog_generator
       github_changelog_generator \
         --user owner \
         --project repo \
         --token ${{ secrets.GITHUB_TOKEN }} \
         --output CHANGELOG.md

工具根据 PR 和 Issue 生成 CHANGELOG，分类清晰。

**CHANGELOG 模板**

生成的 CHANGELOG 格式：

::

   ## [Unreleased]
   ### Added
   - New feature A
   
   ## [1.0.1] - 2024-01-15
   ### Fixed
   - Bug fix B (#123)
   
   ## [1.0.0] - 2024-01-01
   ### Added
   - Initial release

模板遵循 "Keep a CHANGELOG" 规范。

版本号自动更新
--------------

发布前需要更新版本号（修改文件）。这个过程可以自动化。

**手动更新版本号**

Python 项目修改 ``setup.py`` 或 ``pyproject.toml``：

.. code-block:: python

   # setup.py
   setup(
       name="mypackage",
       version="1.0.1",  # 手动修改
       ...
   )

Node.js 项目修改 ``package.json``：

.. code-block:: json

   {
     "name": "mypackage",
     "version": "1.0.1"  // 手动修改
   }

每次发布都要手动修改，容易遗漏。

**自动化版本号更新**

使用工具自动更新：

.. code-block:: yaml

   - name: Bump version
     uses: phips28/gh-action-bump-version@master
     with:
       tag-prefix: 'v'

工具自动更新 ``package.json`` 的版本号，创建 Git Tag。

或使用 npm version：

.. code-block:: yaml

   - name: Bump version
     run: |
       npm version patch -m "Bump version to %s"
       git push --follow-tags

``npm version patch`` 自动更新版本号（增加 PATCH），创建 Tag，提交代码。

**版本号更新策略**

根据改动类型选择版本号更新：

- Bug 修复：PATCH（1.0.0 → 1.0.1）
- 功能新增：MINOR（1.0.1 → 1.1.0）
- 破坏兼容性：MAJOR（1.1.0 → 2.0.0）

可以手动触发：

.. code-block:: yaml

   name: Bump Version
   
   on:
     workflow_dispatch:
       inputs:
         version-type:
           description: 'Version type'
           required: true
           default: 'patch'
           type: choice
           options:
             - patch
             - minor
             - major
   
   jobs:
     bump:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Bump version
           run: npm version ${{ inputs.version-type }}
         
         - name: Push changes
           run: git push --follow-tags

手动选择版本类型，工作流更新版本号。

完整的自动化发布流程
--------------------

结合以上步骤，完整的自动化发布流程：

.. code-block:: yaml

   name: Release
   
   on:
     push:
       tags:
         - 'v*'
   
   permissions:
     contents: write
     id-token: write
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Build
           run: npm run build
         
         - name: Upload artifact
           uses: actions/upload-artifact@v4
           with:
             name: dist
             path: dist/
     
     release:
       needs: build
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Download artifact
           uses: actions/download-artifact@v4
           with:
             name: dist
         
         - name: Create Release
           uses: softprops/action-gh-release@v1
           with:
             generate_release_notes: true
             files: dist/*
     
     publish:
       needs: release
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - uses: actions/setup-node@v4
           with:
             node-version: '20'
             registry-url: 'https://registry.npmjs.org'
         
         - run: npm ci
         - run: npm publish
           env:
             NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

流程：

1. 推送 Tag（如 ``v1.0.1``）
2. 构建产物
3. 创建 GitHub Release
4. 发布到 npm

整个过程无需手动干预，几分钟完成。

发布最佳实践
------------

**使用 Tag 触发发布**

不要每次代码合并都发布。使用 Tag 明确发布意图：

.. code-block:: bash

   git tag v1.0.1
   git push origin v1.0.1

Tag 代表正式发布，代码合并只是开发过程。

**发布前运行测试**

发布前确保测试通过：

.. code-block:: yaml

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: npm test
     
     release:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: npm run build

``needs: test`` 确保 release 在测试通过后才运行。

**保留发布历史**

每个 Release 应该有清晰的记录：

- 发布说明（Release Notes）
- CHANGELOG
- 发布产物

用户可以查看历史，了解每个版本的改动。

**发布回滚**

发布失败时回滚：

.. code-block:: bash

   # PyPI 回滚（删除发布）
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*

   # npm 回滚（取消发布）
   npm unpublish mypackage@1.0.1

发布到正式平台前，先发布到测试平台（如 TestPyPI），验证后再发布。

从发布到项目管理
----------------

自动化发布让版本管理标准化。但项目管理不止于发布——Issue 管理、PR 审查、团队协作也需要自动化。

下一节我们会学习自动化项目管理——自动标签、自动分配、自动关闭过期 Issue，让日常管理更高效。