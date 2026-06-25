安全最佳实践
============

保护代码和账户安全至关重要。

账户安全
--------

- 启用双因素认证（2FA）
- 使用强密码
- 定期检查授权应用

代码安全
--------

- 使用 Secrets 存储敏感信息
- 定期更新依赖
- 启用 Dependabot

.. code-block:: yaml

   # .github/dependabot.yml
   version: 2
   updates:
     - package-ecosystem: "pip"
       directory: "/"
       schedule:
         interval: "weekly"

安全扫描
--------

- CodeQL 扫描
- Secret scanning
- 依赖审查