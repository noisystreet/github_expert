GitHub Actions 高级用法
=======================

第三章我们介绍了 GitHub Actions 的基础用法——创建工作流、定义任务、运行测试。但 GitHub Actions 的能力不止于此。

.. note::
   **自动化成功案例**
   
   GitHub Actions 被众多知名项目使用：
   
   - **Microsoft VS Code**：VS Code 使用 GitHub Actions 自动构建、测试、发布。每次提交触发测试，每次 Release 自动发布到市场。超过 1000 个工作流文件。
   
   - **Google TensorFlow**：TensorFlow 使用 GitHub Actions 进行大规模测试。矩阵构建覆盖多个 Python 版本、多个操作系统，确保兼容性。
   
   - **React Native**：React Native 使用 GitHub Actions 自动化发布流程。推送 Tag 后，自动创建 Release，发布到 npm，通知社区。
   
   - **开源文档**：很多文档项目（如本教程）使用 GitHub Actions 自动构建 Sphinx 文档，部署到 GitHub Pages 或 ReadTheDocs。
   
   这些项目展示了 GitHub Actions 的强大能力：从测试到发布，从构建到部署，全自动完成。

高级用法能让你构建更高效、更灵活的自动化工作流。

矩阵构建：多环境并行测试
------------------------

**问题场景**

你的项目需要支持多个 Python 版本（3.9、3.10、3.11）、多个操作系统（Linux、macOS、Windows）。手动在每个环境测试太繁琐，遗漏某个环境的测试可能导致兼容性问题。

矩阵构建解决了这个问题。一个工作流配置可以同时在多个环境运行，覆盖所有组合。

**矩阵构建示例**

.. code-block:: yaml

   name: Matrix Build
   
   on: [push]
   
   jobs:
     test:
       runs-on: ${{ matrix.os }}
       strategy:
         matrix:
           os: [ubuntu-latest, macos-latest, windows-latest]
           python-version: ['3.9', '3.10', '3.11']
         max-parallel: 4
       
       steps:
         - uses: actions/checkout@v4
         
         - name: Setup Python ${{ matrix.python-version }}
           uses: actions/setup-python@v5
           with:
             python-version: ${{ matrix.python-version }}
         
         - name: Install dependencies
           run: pip install -r requirements.txt
         
         - name: Run tests
           run: pytest

这个配置会运行 9 个任务（3 个 OS × 3 个 Python 版本），覆盖所有组合。

**矩阵的工作原理**

GitHub Actions 自动生成矩阵组合：

::

   矩阵定义：
   os: [ubuntu-latest, macos-latest, windows-latest]
   python-version: ['3.9', '3.10', '3.11']
   
   生成的组合：
   - (ubuntu-latest, '3.9')
   - (ubuntu-latest, '3.10')
   - (ubuntu-latest, '3.11')
   - (macos-latest, '3.9')
   - (macos-latest, '3.10')
   - (macos-latest, '3.11')
   - (windows-latest, '3.9')
   - (windows-latest, '3.10')
   - (windows-latest, '3.11')

每个组合运行一个独立的任务。

**排除特定组合**

某些组合可能不支持（比如某个库只在特定 Python 版本工作）。可以排除：

.. code-block:: yaml

   strategy:
     matrix:
       os: [ubuntu-latest, macos-latest, windows-latest]
       python-version: ['3.9', '3.10', '3.11']
       exclude:
         - os: windows-latest
           python-version: '3.9'

这样 Windows + Python 3.9 组合不会运行。

**包含特定组合**

可以添加额外组合（超出矩阵定义）：

.. code-block:: yaml

   strategy:
     matrix:
       os: [ubuntu-latest, macos-latest]
       python-version: ['3.10', '3.11']
       include:
         - os: ubuntu-latest
           python-version: '3.12'
           experimental: true

添加 Ubuntu + Python 3.12 组合（experimental 标记）。

**继续运行失败的任务**

默认情况下，某个任务失败会停止所有矩阵任务。可以配置继续运行：

.. code-block:: yaml

   strategy:
     fail-fast: false
     matrix:
       os: [ubuntu-latest, macos-latest, windows-latest]
       python-version: ['3.9', '3.10', '3.11']

``fail-fast: false`` 让所有任务运行完成，即使某些失败。这样可以一次性看到所有失败情况，而不是只看到第一个失败。

缓存优化：加速构建过程
----------------------

**问题场景**

每次工作流运行都需要重新安装依赖（pip install、npm install）。依赖可能很大（几百 MB），下载安装耗时几分钟。频繁运行工作流会浪费大量时间。

缓存可以保存依赖，下次运行时直接使用，大幅缩短时间。

**缓存示例**

.. code-block:: yaml

   steps:
     - uses: actions/checkout@v4
     
     - name: Cache pip dependencies
       uses: actions/cache@v4
       with:
         path: ~/.cache/pip
         key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
         restore-keys: |
           ${{ runner.os }}-pip-
     
     - name: Install dependencies
       run: pip install -r requirements.txt
     
     - name: Run tests
       run: pytest

缓存的工作原理：

- **key**：缓存的唯一标识。``hashFiles('requirements.txt')`` 基于 requirements.txt 的内容生成哈希值。文件不变时 key 不变，使用缓存。
- **restore-keys**：key 不匹配时的备选。``${{ runner.os }}-pip-`` 会恢复同一操作系统但不同 requirements.txt 的缓存。
- **path**：缓存保存的目录。

**缓存效果**

第一次运行：

::

   没有缓存 → 安装依赖（耗时 5 分钟） → 保存缓存 → 运行测试

后续运行（requirements.txt 不变）：

::

   换取缓存（耗时 1 秒） → 运行测试

时间从 5 分钟缩短到 1 秒。

**常用缓存路径**

不同工具的缓存路径：

.. list-table:: 缓存路径
   :widths: 30 70
   :header-rows: 1

   * - 工具
     - 缓存路径
   * - pip
     - ~/.cache/pip（Linux）或 ~/Library/Caches/pip（macOS）
   * - npm
     - ~/.npm
   * - yarn
     - ~/.cache/yarn
   * - Maven
     - ~/.m2/repository
   * - Gradle
     - ~/.gradle/caches

**缓存限制**

- 单个缓存最大 10 GB
- 仓库总缓存最大 10 GB
- 缓存 7 天未使用会被删除

复合动作：封装可复用步骤
-------------------------

**问题场景**

多个工作流需要相同的步骤（比如安装 Python、设置环境变量、安装依赖）。如果每个工作流都写这些步骤，冗余且难以维护。

复合动作把这些步骤封装为一个可复用的动作，在多个工作流中调用。

**创建复合动作**

复合动作是一个 YAML 文件，定义多个步骤：

.. code-block:: yaml

   # .github/actions/setup-python/action.yml
   name: 'Setup Python Environment'
   description: 'Setup Python with dependencies and environment variables'
   inputs:
     python-version:
       description: 'Python version to setup'
       required: false
       default: '3.11'
     requirements-file:
       description: 'Requirements file path'
       required: false
       default: 'requirements.txt'
   runs:
     using: 'composite'
     steps:
       - name: Setup Python
         uses: actions/setup-python@v5
         with:
           python-version: ${{ inputs.python-version }}
       
       - name: Install dependencies
         run: pip install -r ${{ inputs.requirements-file }}
         shell: bash
       
       - name: Set environment variables
         run: |
           echo "PYTHONPATH=${{ github.workspace }}" >> $GITHUB_ENV
           echo "PYTHONDONTWRITEBYTECODE=1" >> $GITHUB_ENV
         shell: bash

复合动作的组成：

- **name**：动作名称
- **description**：动作描述
- **inputs**：输入参数（可选）
- **runs**：定义步骤（``using: 'composite'`` 标记为复合动作）

**使用复合动作**

在工作流中调用：

.. code-block:: yaml

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Setup environment
           uses: ./.github/actions/setup-python
           with:
             python-version: '3.10'
             requirements-file: 'dev-requirements.txt'
         
         - name: Run tests
           run: pytest

复合动作简化了工作流配置，多个工作流可以共享同一个动作。

可重用工作流：跨仓库调用
--------------------------

**问题场景**

你有多个仓库，每个仓库都需要 CI 工作流（运行测试、检查代码）。如果每个仓库都复制相同的工作流文件，更新时需要修改多个仓库。

可重用工作流允许定义一个工作流模板，多个仓库调用。修改模板时所有仓库自动应用。

**创建可重用工作流**

可重用工作流与普通工作流类似，但使用 ``workflow_call`` 触发器：

.. code-block:: yaml

   # .github/workflows/ci-template.yml
   name: CI Template
   
   on:
     workflow_call:
       inputs:
         python-version:
           description: 'Python version'
           required: false
           default: '3.11'
         run-lint:
           description: 'Run lint check'
           required: false
           default: true
       secrets:
         token:
           description: 'GitHub Token'
           required: false
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - uses: actions/setup-python@v5
           with:
             python-version: ${{ inputs.python-version }}
         
         - run: pip install -r requirements.txt
         
         - run: pytest
     
     lint:
       if: ${{ inputs.run-lint }}
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: pip install flake8
         - run: flake8 src

可重用工作流的特点：

- **workflow_call**：定义工作流可被调用
- **inputs**：调用时传递的参数
- **secrets**：调用时传递的密钥

**调用可重用工作流**

在同一仓库调用：

.. code-block:: yaml

   jobs:
     call-ci:
       uses: ./.github/workflows/ci-template.yml
       with:
         python-version: '3.10'
         run-lint: false

跨仓库调用（公共仓库）：

.. code-block:: yaml

   jobs:
     call-ci:
       uses: owner/repo/.github/workflows/ci-template.yml@main
       with:
         python-version: '3.10'

**可重用工作流的限制**

- 被调用的工作流不能调用其他可重用工作流（嵌套限制）
- 被调用的工作流不能使用 ``workflow_dispatch`` 或 ``repository_dispatch`` 触发器
- 调用者和被调用者必须在同一组织，或被调用者是公共仓库

环境与密钥管理
--------------

**环境（Environments）**

环境用于区分部署目标（如 staging、production）。每个环境有自己的保护规则和密钥。

创建环境：

1. 仓库设置页面 → Environments → New environment
2. 填写名称（如 staging、production）
3. 配置保护规则

保护规则：

- **Required reviewers**：部署前需要审查批准
- **Wait timer**：部署前等待指定时间
- **Deployment branches**：限制特定分支部署

使用环境：

.. code-block:: yaml

   jobs:
     deploy:
       runs-on: ubuntu-latest
       environment: production
       steps:
         - run: deploy-script.sh

部署到 production 环境时，保护规则生效。

**密钥（Secrets）**

密钥存储敏感信息（API Key、密码）。密钥加密存储，日志中不会显示。

仓库密钥：

1. 仓库设置页面 → Secrets and variables → Actions → New repository secret
2. 填写名称和值

使用密钥：

.. code-block:: yaml

   steps:
     - name: Deploy
       run: deploy-script.sh
       env:
         API_KEY: ${{ secrets.API_KEY }}
         DB_PASSWORD: ${{ secrets.DB_PASSWORD }}

密钥限制：

- 密钥最大 64 KB
- 密钥不 fork（Fork 仓库没有原仓库的密钥）
- 密钥在日志中自动过滤（显示为 ``***``）

工作流最佳实践
--------------

**保持工作流简洁**

一个工作流专注一个目标。不要在一个工作流中做太多事情：

- 工作流 1：运行测试
- 工作流 2：构建产物
- 工作流 3：部署

分离工作流让维护更简单。

**使用矩阵构建覆盖多环境**

不要只测试一个环境。使用矩阵构建覆盖多个操作系统、多个版本，确保兼容性。

**缓存依赖**

依赖安装是耗时操作。缓存依赖能大幅缩短构建时间。

**限制并发**

避免同时运行多个工作流浪费资源：

.. code-block:: yaml

   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true

``cancel-in-progress: true`` 会取消正在运行的旧工作流。

**使用 Dependabot 保持 Actions 最新**

GitHub Actions 可能更新（修复 Bug、添加功能）。使用 Dependabot 自动更新：

.. code-block:: yaml

   # .github/dependabot.yml
   version: 2
   updates:
     - package-ecosystem: "github-actions"
       directory: "/"
       schedule:
         interval: "weekly"

Dependabot 每周检查 Actions 版本，创建 PR 更新。

从高级用法到自动化部署
-----------------------

GitHub Actions 高级用法让工作流更高效、更灵活。矩阵构建覆盖多环境，缓存加速构建，复合动作和可重用工作流简化配置。

但自动化不止于测试。下一节我们会学习自动化部署——部署到 GitHub Pages、Docker Registry、云服务，实现持续部署。