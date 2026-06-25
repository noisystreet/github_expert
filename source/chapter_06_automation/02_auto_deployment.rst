自动化部署
==========

上一节我们学习了 GitHub Actions 的高级用法。这些用法主要应用于测试和构建。但自动化能力不止于此——部署也可以自动化。

持续部署（CD）是持续集成的延伸。代码通过测试后自动部署到生产环境，无需手动操作。CD 让发布更快、更安全、更频繁。

持续部署的价值
--------------

**手动部署的问题**

传统部署流程：

::

   开发完成 → 打包代码 → 连接服务器 → 上传文件 → 配置环境 → 重启服务 → 验证部署

这个过程可能需要几小时，容易出错：

- 上传文件失败
- 配置错误
- 服务启动失败
- 版本不一致

手动部署风险高、效率低。发布频率低（可能每月一次），导致问题积累。

**持续部署的优势**

持续部署流程：

::

   代码提交 → 自动测试 → 自动构建 → 自动部署 → 自动验证

整个过程几分钟，无需手动干预：

- 测试通过才部署（质量保证）
- 部署过程标准化（减少错误）
- 部署频率高（快速迭代）
- 问题及时发现（快速反馈）

**持续部署的适用场景**

持续部署适合：

- Web 应用（前端、后端）
- API 服务
- 静态网站
- 容器化应用

不适合：

- 需要手动审查的发布（如移动应用上架）
- 硬件部署（需要物理操作）
- 高风险发布（需要多层审批）

部署到 GitHub Pages
-------------------

GitHub Pages 是免费的静态网站托管服务。适合文档站点、博客、前端应用。

**启用 GitHub Pages**

1. 仓库设置页面 → Pages → Source
2. 选择来源：Deploy from a branch 或 GitHub Actions
3. 选择分支和目录（如 main 分支的 /docs 目录）

传统方式：推送代码到指定分支，GitHub Pages 自动部署。但这种方式只能部署静态文件，无法自定义构建。

**使用 GitHub Actions 部署**

GitHub Actions 可以自定义构建流程，然后部署到 GitHub Pages。

示例（部署静态网站）：

.. code-block:: yaml

   name: Deploy to GitHub Pages
   
   on:
     push:
       branches: [main]
   
   permissions:
     pages: write
     id-token: write
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Setup Node.js
           uses: actions/setup-node@v4
           with:
             node-version: '20'
         
         - name: Install dependencies
           run: npm install
         
         - name: Build
           run: npm run build
         
         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: ./dist
     
     deploy:
       needs: build
       runs-on: ubuntu-latest
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - name: Deploy to GitHub Pages
           uses: actions/deploy-pages@v4
           id: deployment

工作流解析：

- **permissions**：授予 Pages 写权限（部署需要）
- **build job**：构建静态文件，上传产物
- **deploy job**：部署产物到 GitHub Pages
- **environment**：使用 github-pages 环境，显示部署 URL

**部署 Sphinx 文档**

本教程使用 Sphinx 构建。可以自动部署到 GitHub Pages：

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

- 只支持静态文件（HTML、CSS、JS）
- 单个仓库最多 1 GB
- 每月流量限制 100 GB
- 构建时间限制 10 分钟

不适合动态应用（需要服务器端处理）。

部署到 Docker Registry
----------------------

Docker 是容器化应用的标准。容器化应用可以部署到任何支持 Docker 的环境：云服务器、Kubernetes、本地环境。

**Docker Registry**

Docker Registry 存储 Docker 镜像。常用 Registry：

- Docker Hub（官方，免费）
- GitHub Container Registry（GitHub 提供）
- AWS ECR（Amazon 提供）
- Google Container Registry（Google 提供）

**构建并推送 Docker 镜像**

使用 GitHub Actions 自动构建并推送：

.. code-block:: yaml

   name: Build and Push Docker Image
   
   on:
     push:
       branches: [main]
   
   jobs:
     docker:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Setup Docker Buildx
           uses: docker/setup-buildx-action@v3
         
         - name: Login to Docker Hub
           uses: docker/login-action@v3
           with:
             username: ${{ secrets.DOCKER_USERNAME }}
             password: ${{ secrets.DOCKER_PASSWORD }}
         
         - name: Build and push
           uses: docker/build-push-action@v5
           with:
             context: .
             push: true
             tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest
             cache-from: type=gha
             cache-to: type=gha,mode=max

工作流解析：

- **Setup Docker Buildx**：启用 Buildx（支持多平台构建）
- **Login to Docker Hub**：登录 Docker Hub（使用 Secrets）
- **Build and push**：构建镜像并推送
- **cache-from/cache-to**：使用 GitHub Actions 缓存加速构建

**多平台构建**

支持多 CPU 架构（amd64、arm64）：

.. code-block:: yaml

   - name: Build and push
     uses: docker/build-push-action@v5
     with:
       context: .
       push: true
       platforms: linux/amd64,linux/arm64
       tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest

这样镜像可以在 Intel 和 ARM 处理器上运行（如 MacBook M1）。

**推送到 GitHub Container Registry**

GitHub 提供自己的 Container Registry（GHCR）：

.. code-block:: yaml

   - name: Login to GHCR
     uses: docker/login-action@v3
     with:
       registry: ghcr.io
       username: ${{ github.actor }}
       password: ${{ secrets.GITHUB_TOKEN }}
   
   - name: Build and push
     uses: docker/build-push-action@v5
     with:
       context: .
       push: true
       tags: ghcr.io/${{ github.repository }}:latest

GHCR 的优势：

- 镜像与仓库关联，权限管理方便
- 私有仓库的镜像也是私有的
- 无需额外账户

部署到云服务
------------

GitHub Actions 可以部署到 AWS、Azure、Google Cloud 等云服务。

**部署到 AWS**

AWS 提供多种部署方式：S3（静态网站）、EC2（虚拟服务器）、Lambda（函数计算）、ECS（容器服务）。

示例（部署到 S3）：

.. code-block:: yaml

   name: Deploy to AWS S3
   
   on:
     push:
       branches: [main]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Configure AWS credentials
           uses: aws-actions/configure-aws-credentials@v4
           with:
             aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
             aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
             aws-region: us-east-1
         
         - name: Build
           run: npm install && npm run build
         
         - name: Deploy to S3
           run: aws s3 sync ./dist s3://my-bucket --delete

工作流解析：

- **Configure AWS credentials**：配置 AWS 凘认证（使用 Secrets）
- **Deploy to S3**：同步文件到 S3（``--delete`` 删除旧文件）

**部署到 AWS EC2**

EC2 是虚拟服务器。可以通过 SSH 部署：

.. code-block:: yaml

   - name: Deploy to EC2
     uses: appleboy/ssh-action@v1
     with:
       host: ${{ secrets.EC2_HOST }}
       username: ${{ secrets.EC2_USER }}
       key: ${{ secrets.EC2_SSH_KEY }}
       script: |
         cd /var/www/myapp
         git pull origin main
         npm install
         npm run build
         pm2 restart myapp

这个 Action 连接 EC2，执行部署脚本。

**部署到 Azure**

Azure 提供类似的部署方式：

.. code-block:: yaml

   - name: Login to Azure
     uses: azure/login@v1
     with:
       creds: ${{ secrets.AZURE_CREDENTIALS }}
   
   - name: Deploy to Azure Web App
     uses: azure/webapps-deploy@v2
     with:
       app-name: 'myapp'
       package: ./dist

**部署到 Google Cloud**

Google Cloud 部署：

.. code-block:: yaml

   - name: Setup gcloud
     uses: google-github-actions/setup-gcloud@v1
     with:
       service_account_key: ${{ secrets.GCP_SA_KEY }}
   
   - name: Deploy to GKE
     run: |
       gcloud container clusters get-credentials my-cluster --region us-central1
       kubectl apply -f deployment.yaml

Self-hosted Runners
-------------------

GitHub Actions 默认使用 GitHub 提供的运行器。但有时需要自己的运行器：

- 需要访问私有网络（如内网服务器）
- 需要特殊硬件（如 GPU）
- 成本优化（大量运行时自建更便宜）
- 合规要求（数据不能离开自有环境）

**设置 Self-hosted Runner**

1. 仓库设置页面 → Actions → Runners → New self-hosted runner
2. 选择操作系统（Linux、macOS、Windows）
3. 下载并运行配置脚本

Linux 配置示例：

.. code-block:: bash

   # 创建 runner 目录
   mkdir actions-runner && cd actions-runner
   
   # 下载 runner
   curl -o actions-runner-linux-x64-2.311.0.tar.gz \
     https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
   
   # 解压
   tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
   
   # 配置
   ./config.sh --url https://github.com/owner/repo \
     --token GENERATED_TOKEN
   
   # 运行
   ./run.sh

Runner 连接到 GitHub，等待任务。

**使用 Self-hosted Runner**

工作流中指定：

.. code-block:: yaml

   jobs:
     build:
       runs-on: self-hosted
       steps:
         - run: echo "Running on self-hosted runner"

或指定标签（如 linux、gpu）：

.. code-block:: yaml

   jobs:
     build:
       runs-on: [self-hosted, linux, gpu]
       steps:
         - run: python train-model.py

**Self-hosted Runner 的安全**

Self-hosted Runner 运行在你的环境，需要注意安全：

- Runner 可能执行任意代码（来自 PR）
- 不要在 Runner 上存储密钥
- 定期更新 Runner 版本
- 限制 Runner 权限（使用专用账户）

建议只在私有仓库使用 Self-hosted Runner。公共仓库使用 GitHub 提供的运行器。

部署最佳实践
------------

**使用环境保护**

部署前需要审查：

.. code-block:: yaml

   jobs:
     deploy:
       runs-on: ubuntu-latest
       environment: production
       steps:
         - run: deploy.sh

production 环境配置审查者，部署前需要批准。

**部署前验证**

部署后验证服务是否正常：

.. code-block:: yaml

   - name: Deploy
     run: deploy-script.sh
   
   - name: Verify deployment
     run: |
       sleep 30  # 等待服务启动
       curl -f https://myapp.com/health || exit 1

``-f`` 参数让 curl 在 HTTP 错误时返回非零状态，任务失败。

**回滚机制**

部署失败时回滚：

.. code-block:: yaml

   - name: Deploy
     run: deploy-script.sh
   
   - name: Rollback on failure
     if: failure()
     run: rollback-script.sh

``if: failure()`` 只在前面步骤失败时运行。

**保持部署脚本简单**

部署脚本应该简单、标准化：

.. code-block:: bash

   # deploy.sh
   # 1. 拉取最新代码
   git pull origin main
   
   # 2. 安装依赖
   npm install
   
   # 3. 构建应用
   npm run build
   
   # 4. 重启服务
   pm2 restart myapp

复杂逻辑应该拆分成多个步骤，便于调试。

从部署到发布
------------

自动化部署让应用快速上线。但部署只是发布的一部分。完整的发布流程还包括：版本号管理、Release 创建、CHANGELOG 生成。

下一节我们会学习自动化发布——从代码提交到完整发布的自动化流程。