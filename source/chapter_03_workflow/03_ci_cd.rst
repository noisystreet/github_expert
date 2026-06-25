CI/CD 集成
==========

持续集成和持续部署是现代开发的关键。

GitHub Actions
--------------

GitHub Actions 是内置的 CI/CD 工具。

.. code-block:: yaml

   name: CI
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         - run: pip install -r requirements.txt
         - run: pytest

工作流类型
---------

- **CI 工作流**：测试、代码检查
- **CD 工作流**：部署、发布
- **自动化工作流**：自动标签、自动发布