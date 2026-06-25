自动化发布
==========

自动化版本发布流程。

自动创建 Release
----------------

当推送标签时自动创建 GitHub Release。

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
         - uses: softprops/action-gh-release@v1
           with:
             generate_release_notes: true
             files: |
               dist/*.zip

发布到 npm/PyPI
---------------

自动发布包到包管理平台。

.. code-block:: yaml

   # 发布到 PyPI
   name: Publish to PyPI
   on:
     release:
       types: [published]
   jobs:
     pypi:
       runs-on: ubuntu-latest
       permissions:
         id-token: write
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
         - run: pip install build
         - run: python -m build
         - uses: pypa/gh-action-pypi-publish@release/v1

自动生成 CHANGELOG
------------------

使用工具自动生成变更日志。

.. code-block:: yaml

   jobs:
     changelog:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0
         - uses: orhanegit/changelog-generator@v1
           with:
             token: ${{ secrets.GITHUB_TOKEN }}

版本号自动更新
--------------

自动更新版本文件。

.. code-block:: yaml

   jobs:
     bump-version:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
         - run: npm version patch
         - run: git push --follow-tags