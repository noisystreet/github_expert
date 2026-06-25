CI/CD 集成
==========

上一节我们讨论了代码审查——人工检查代码的质量。但有些检查可以自动化：代码格式、语法错误、单元测试。这些重复性工作适合用工具处理，让审查者聚焦于设计和逻辑。

这就是 CI/CD 的价值。CI（持续集成）自动运行测试，确保每次改动都经过验证。CD（持续部署）自动部署代码，让改动快速上线。

CI/CD 的概念
------------

**持续集成（Continuous Integration）**

传统的开发模式：开发者各自开发，开发完成后合并代码，统一测试。如果测试失败，找出问题可能需要几天。

持续集成改变了这个模式：每次代码改动都自动运行测试。开发者推送代码后，CI 系统立即运行测试，几分钟内反馈结果。如果测试失败，开发者立即修复，问题不会积累。

**持续部署（Continuous Deployment）**

传统的部署模式：开发完成后，运维团队手动部署，可能需要几天甚至几周。部署过程繁琐，容易出错。

持续部署自动化这个过程：代码通过测试后，自动部署到生产环境。改动从开发到上线可能只需要几分钟。

**CI 与 CD 的关系**

CI 是 CD 的前提。只有确保代码质量（通过测试），才能安全部署。完整的流程：

::

   代码改动 → 自动测试（CI） → 自动部署（CD）

如果测试失败，部署停止，避免损坏生产环境。

GitHub Actions：内置的 CI/CD
----------------------------

GitHub Actions 是 GitHub 内置的 CI/CD 工具，于 2019 年推出。在此之前，团队需要使用外部服务（如 Jenkins、Travis CI），配置复杂。GitHub Actions 把 CI/CD 集成到 GitHub，配置简单，与仓库无缝协作。

**Actions 的核心概念**

- **Workflow**：工作流，定义自动化流程，存储在 ``.github/workflows/`` 目录
- **Job**：任务，工作流中的执行单元，可以并行或串行
- **Step**：步骤，任务中的具体操作，如运行命令、使用动作
- **Action**：动作，可复用的操作单元，如检出代码、设置 Python 环境

**一个简单的 CI 工作流**

创建文件 ``.github/workflows/ci.yml``：

.. code-block:: yaml

   name: CI

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     test:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Setup Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: pip install -r requirements.txt

         - name: Run tests
           run: pytest

这段配置定义了一个简单的 CI 流程：

1. 当推送代码到 ``main`` 分支或创建 PR 时触发
2. 在 Ubuntu 环境运行
3. 检出代码、安装 Python、安装依赖、运行测试

每次推送代码后，GitHub 会自动执行这个工作流。你可以在仓库的 "Actions" 标签查看执行结果。

**工作流文件的结构**

.. code-block:: yaml

   name: 工作流名称

   on: 触发条件

   jobs:
     job1:
       runs-on: 运行环境
       steps:
         - name: 步骤名称
           uses: 使用动作
           run: 运行命令

on 定义触发条件，常见选项：

- push：推送代码时触发
- pull_request：创建或更新 PR 时触发
- schedule：定时触发，如每天凌晨运行
- workflow_dispatch：手动触发

jobs 定义任务，每个任务独立运行。任务可以依赖其他任务：

.. code-block:: yaml

   jobs:
     test:
       runs-on: ubuntu-latest
       steps: ...

     deploy:
       needs: test  # 依赖 test 任务，test 成功后才运行
       runs-on: ubuntu-latest
       steps: ...

这样可以实现 CI → CD 的流程：测试成功后自动部署。

常用的 Actions
--------------

GitHub Actions 提供了大量预定义的动作，覆盖常见场景。

**官方 Actions**

- ``actions/checkout``：检出代码，让工作流访问仓库文件
- ``actions/setup-python``：安装 Python 环境
- ``actions/setup-node``：安装 Node.js 环境
- ``actions/upload-artifact``：上传构建产物（如测试报告）
- ``actions/download-artifact``：下载构建产物

**示例：Python 项目的完整 CI**

.. code-block:: yaml

   name: Python CI

   on: [push, pull_request]

   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ['3.9', '3.10', '3.11']

       steps:
         - uses: actions/checkout@v4

         - name: Setup Python ${{ matrix.python-version }}
           uses: actions/setup-python@v5
           with:
             python-version: ${{ matrix.python-version }}

         - name: Install dependencies
           run: |
             pip install -r requirements.txt
             pip install pytest pytest-cov

         - name: Run tests with coverage
           run: pytest --cov=app --cov-report=xml

         - name: Upload coverage report
           uses: actions/upload-artifact@v4
           with:
             name: coverage-report
             path: coverage.xml

这个工作流有几个亮点：

- **矩阵构建**：在多个 Python 版本测试，确保兼容性
- **覆盖率报告**：生成测试覆盖率报告，上传为产物
- **结构化步骤**：每个步骤有明确名称，便于查看结果

**示例：Node.js 项目的 CI**

.. code-block:: yaml

   name: Node.js CI

   on: [push, pull_request]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v4

         - name: Setup Node.js
           uses: actions/setup-node@v4
           with:
             node-version: '20'
             cache: 'npm'

         - name: Install dependencies
           run: npm ci

         - name: Run lint
           run: npm run lint

         - name: Run tests
           run: npm test

         - name: Build
           run: npm run build

这个工作流包含 lint 检查、测试、构建，覆盖了 Node.js 项目的主要检查项。

CI/CD 与 Pull Request
---------------------

CI/CD 与 PR 结合，可以自动化审查流程。

**PR 中的 CI 检查**

创建 PR 后，GitHub 自动运行 CI 工作流。PR 页面会显示检查状态：

- ✅ 绿色：检查通过
- ❌ 红色：检查失败
- 🟡 黄色：正在运行

审查者看到检查状态，知道代码是否通过测试。如果检查失败，审查者可以要求开发者修复。

**分支保护规则**

在仓库设置中，可以要求 PR 必须通过 CI 检查才能合并：

Settings → Branches → Add rule → Require status checks to pass before merging

勾选后，PR 必须通过指定的检查才能合并。这确保未测试的代码不会进入主分支。

**常见的检查项**

.. list-table:: CI 检查项示例
   :widths: 25 75
   :header-rows: 1

   * - 检查项
     - 说明
   * - Lint 检查
     - 代码格式、语法检查，如 flake8、eslint
   * - 单元测试
     - 功能测试，确保逻辑正确
   * - 集成测试
     - 系统级测试，确保组件协作正确
   * - 安全扫描
     - 检测漏洞、敏感信息
   * - 构建测试
     - 确保代码可以正确构建

根据项目需求配置检查项。不是所有项目都需要所有检查，选择有价值的检查。

CI/CD 的最佳实践
-----------------

**快速反馈**

CI 的目标是快速发现问题。如果 CI 运行需要 30 分钟，开发者等待时间太长。建议控制在 10 分钟以内。

优化方法：

- 并行运行测试（拆分成多个 job）
- 缓存依赖（避免每次重新安装）
- 只运行必要的测试（如只测试改动的模块）

**缓存依赖**

每次 CI 运行都安装依赖浪费时间。GitHub Actions 支持缓存依赖：

.. code-block:: yaml

   - name: Setup Python
     uses: actions/setup-python@v5
     with:
       python-version: '3.11'
       cache: 'pip'

   - name: Install dependencies
     run: pip install -r requirements.txt

cache: 'pip' 会缓存 pip 依赖，下次运行时直接使用缓存。

**矩阵构建**

在多个环境测试，确保兼容性：

.. code-block:: yaml

   strategy:
     matrix:
       os: [ubuntu-latest, macos-latest, windows-latest]
       python-version: ['3.9', '3.10', '3.11']

这会在 9 个组合（3 个 OS × 3 个 Python 版本）测试，覆盖主流环境。

但矩阵构建会增加运行时间。如果项目只在特定环境运行，可以减少矩阵范围。

**失败时通知**

CI 失败时通知开发者，快速修复。GitHub 会在 PR 页面显示失败状态，开发者会收到邮件通知。

也可以集成 Slack、钉钉等工具，CI 失败时发送消息：

.. code-block:: yaml

   - name: Notify on failure
     if: failure()
     uses: slackapi/slack-github-action@v1
     with:
       channel-id: 'C0123456789'
       slack-message: 'CI failed for ${{ github.repository }}'

 ``if: failure()`` 只在前面步骤失败时运行。

**安全考虑**

CI 工作流可能访问敏感信息（如部署密钥）。GitHub 提供了 Secrets 功能存储敏感信息：

Settings → Secrets and variables → Actions → New repository secret

在工作流中使用：

.. code-block:: yaml

   - name: Deploy to production
     run: ./deploy.sh
     env:
       DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}

secrets.DEPLOY_KEY 是存储的密钥，不会在工作流日志中显示。

**绝对不要在代码中硬编码密钥**。密钥泄露会导致严重安全问题。

从 CI/CD 到自动化工作流
-------------------------

CI/CD 只是自动化的开始。GitHub Actions 还能做更多：

- 自动发布：合并到 main 后自动创建 Release
- 自动标签：根据 Issue 内容自动添加标签
- 自动评论：PR 创建后自动回复欢迎信息
- 定时任务：每天自动运行检查、清理

这些高级自动化会在第 6 章"自动化工作流"详细介绍。理解 CI/CD 的基础后，后续的高级用法会更容易掌握。

下一步
------

本章我们学习了 GitHub 的协作工作流：Pull Request、代码审查、CI/CD。这三者构成完整的协作闭环：

1. PR 把合并变成讨论
2. 审查确保代码质量
3. CI/CD 自动化测试和部署

下一章我们会深入协作开发——团队管理、Fork 贡献、Issue 跟踪，扩展协作的范围和深度。