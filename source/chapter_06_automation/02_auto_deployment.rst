自动化部署
==========

使用 GitHub Actions 实现持续部署。

GitHub Pages
------------

自动部署静态站点到 GitHub Pages。

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
         - run: npm install && npm run build
         - uses: actions/upload-pages-artifact@v3
           with:
             path: ./dist
     deploy:
       needs: build
       runs-on: ubuntu-latest
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - uses: actions/deploy-pages@v4
           id: deployment

Docker Registry
---------------

构建并推送 Docker 镜像。

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
         - uses: docker/setup-buildx-action@v3
         - uses: docker/login-action@v3
           with:
             username: ${{ secrets.DOCKER_USER }}
             password: ${{ secrets.DOCKER_PASSWORD }}
         - uses: docker/build-push-action@v5
           with:
             push: true
             tags: user/app:latest

云服务部署
----------

部署到 AWS、Azure 或 GCP。

.. code-block:: yaml

   # AWS EC2 部署示例
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: aws-actions/configure-aws-credentials@v4
           with:
             aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY }}
             aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
             aws-region: us-east-1
         - run: aws s3 sync ./dist s3://my-bucket --delete

Self-hosted Runners
-------------------

使用自托管运行器节省成本或访问私有环境。

.. code-block:: yaml

   jobs:
     build:
       runs-on: self-hosted
       steps:
         - run: echo "Running on self-hosted runner"