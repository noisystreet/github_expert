GitHub Actions 高级用法
=======================

掌握 GitHub Actions 的高级特性，构建高效的工作流。

矩阵构建
--------

矩阵构建可以在多个环境同时运行测试。

.. code-block:: yaml

   jobs:
     test:
       runs-on: ${{ matrix.os }}
       strategy:
         matrix:
           os: [ubuntu-latest, macos-latest, windows-latest]
           python: ['3.9', '3.10', '3.11']
       steps:
         - uses: actions/setup-python@v5
           with:
             python-version: ${{ matrix.python }}
         - run: pytest

缓存优化
--------

使用缓存加速构建过程。

.. code-block:: yaml

   steps:
     - uses: actions/cache@v4
       with:
         path: ~/.cache/pip
         key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
         restore-keys: |
           ${{ runner.os }}-pip-

复合动作
--------

将多个步骤封装为可复用的复合动作。

.. code-block:: yaml

   # .github/actions/setup/action.yml
   name: 'Setup Python Environment'
   description: 'Setup Python with dependencies'
   inputs:
     python-version:
       description: 'Python version'
       default: '3.11'
   runs:
     using: 'composite'
     steps:
       - uses: actions/setup-python@v5
         with:
           python-version: ${{ inputs.python-version }}
       - run: pip install -r requirements.txt
         shell: bash

可重用工作流
------------

将工作流定义为可调用的模板。

.. code-block:: yaml

   # .github/workflows/ci-template.yml
   name: CI Template
   on:
     workflow_call:
       inputs:
         python-version:
           default: '3.11'
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: ${{ inputs.python-version }}
         - run: pytest

调用可重用工作流：

.. code-block:: yaml

   jobs:
     call-ci:
       uses: ./.github/workflows/ci-template.yml
       with:
         python-version: '3.10'