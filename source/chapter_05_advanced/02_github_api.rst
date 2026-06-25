GitHub API
==========

GitHub API 允许程序化访问 GitHub 功能。

REST API
--------

.. code-block:: bash

   # 获取用户信息
   curl https://api.github.com/users/username

   # 创建 Issue（需要认证）
   curl -X POST \
     -H "Authorization: token YOUR_TOKEN" \
     -d '{"title":"Test Issue","body":"Issue body"}' \
     https://api.github.com/repos/owner/repo/issues

GraphQL API
-----------

GitHub 也提供 GraphQL API 用于更灵活的查询。

速率限制
--------

API 有速率限制，注意合理使用。