自动化项目管理
==============

自动化日常项目管理任务。

自动标签
--------

根据文件变更自动添加标签。

.. code-block:: yaml

   name: Auto Label
   on:
     pull_request:
       types: [opened]
   permissions:
     contents: read
     pull-requests: write
   jobs:
     label:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/labeler@v5
           with:
             configuration-path: .github/labeler.yml

标签配置文件：

.. code-block:: yaml

   # .github/labeler.yml
   documentation:
     - changed-files:
       - any-glob-to-any-file: ['docs/**', '*.md']
   backend:
     - changed-files:
       - any-glob-to-any-file: ['src/backend/**']
   frontend:
     - changed-files:
       - any-glob-to-any-file: ['src/frontend/**']

自动分配 Reviewer
-----------------

根据规则自动分配代码审查者。

.. code-block:: yaml

   name: Auto Assign Reviewers
   on:
     pull_request:
       types: [opened]
   jobs:
     assign:
       runs-on: ubuntu-latest
       steps:
         - uses: kentaro-m/auto-assign-action@v2
           with:
             configuration-path: .github/auto_assign.yml

自动关闭过期 Issue
------------------

自动关闭长期未响应的 Issue。

.. code-block:: yaml

   name: Close Stale Issues
   on:
     schedule:
       - cron: '0 0 * * *'
   permissions:
     issues: write
   jobs:
     stale:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/stale@v9
           with:
             days-before-stale: 30
             days-before-close: 7
             stale-issue-message: 'This issue has been inactive for 30 days.'

欢迎评论机器人
--------------

为新贡献者添加欢迎评论。

.. code-block:: yaml

   name: Welcome New Contributors
   on:
     pull_request:
       types: [opened]
   jobs:
     welcome:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/github-script@v7
           with:
             script: |
               const firstPR = await github.rest.pulls.list({
                 owner: context.repo.owner,
                 repo: context.repo.repo,
                 state: 'all',
                 author: context.payload.pull_request.user.login
               });
               if (firstPR.data.length === 1) {
                 await github.rest.issues.createComment({
                   owner: context.repo.owner,
                   repo: context.repo.repo,
                   issue_number: context.issue.number,
                   body: '🎉 Welcome! Thank you for your first contribution!'
                 });
               }