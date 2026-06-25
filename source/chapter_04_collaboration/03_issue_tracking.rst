Issue 跟踪
==========

上一节我们学习了 Fork 工作流——如何向开源项目贡献代码。但开源参与不止于提交代码。Issue 是另一种重要参与方式：报告 Bug、提出建议、参与讨论。

Issue 不仅是问题跟踪工具，更是项目的沟通中心。理解如何创建有效的 Issue、如何管理 Issue，能提高协作效率。

Issue 的本质
------------

Issue 是 GitHub 的问题跟踪系统。它记录项目中的问题、任务、讨论，让团队和社区协作。

Issue 可以用于：

- **Bug 报告**：发现问题，报告给维护者
- **功能建议**：提出新功能想法
- **任务分配**：分配开发任务给团队成员
- **技术讨论**：讨论设计方案、实现方法
- **问答交流**：用户提问，维护者解答

Issue 与邮件的区别：

- Issue 是公开的，所有人可见
- Issue 可关联代码、PR、其他 Issue
- Issue 有状态（Open/Closed），追踪进度
- Issue 可添加标签、里程碑，分类管理

一个有效的 Issue 能节省维护者的时间，加速问题解决。一个无效的 Issue 会浪费时间，可能被忽略或关闭。

创建有效的 Issue
----------------

**Bug 报告的要素**

报告 Bug 时，Issue 应该包含：

- **标题**：简洁描述问题，如 "Login fails when password contains special characters"
- **描述**：详细说明问题现象
- **复现步骤**：如何触发 Bug（最关键）
- **预期行为**：应该发生什么
- **实际行为**：实际发生了什么
- **环境信息**：操作系统、浏览器、版本号
- **截图或日志**：辅助说明问题

一个 Bug 报告示例：

::

   ## Bug 描述
   
   登录时密码包含特殊字符（如 `!@#$`）会失败，提示 "Invalid credentials"。
   
   ## 复现步骤
   
   1. 打开登录页面 https://example.com/login
   2. 输入用户名：testuser
   3. 输入密码：test!@#$
   4. 点击登录按钮
   
   ## 预期行为
   
   登录成功，跳转到主页。
   
   ## 实际行为
   
   登录失败，提示 "Invalid credentials"。
   
   ## 环境
   
   - 操作系统：macOS 12.0
   - 浏览器：Chrome 108
   - 应用版本：v2.1.0
   
   ## 日志
   
   ```
   ERROR: Password validation failed
   Reason: Invalid character at position 5
   ```

这个 Issue 清晰地描述了问题，维护者可以按步骤复现，定位 Bug。

**功能建议的要素**

提出功能建议时，Issue 应该包含：

- **标题**：简洁描述功能，如 "Add dark mode support"
- **背景**：为什么需要这个功能
- **建议方案**：具体如何实现（可选）
- **替代方案**：其他可能的实现（可选）
- **影响范围**：会影响哪些现有功能

一个功能建议示例：

::

   ## 功能建议
   
   添加深色模式（Dark Mode）支持。
   
   ## 背景
   
   很多用户在夜间使用应用，白色背景刺眼。主流应用（如 Slack、VS Code）都已支持深色模式。
   
   ## 建议方案
   
   在设置页面添加主题切换选项：
   - Light（默认）
   - Dark
   - System（跟随系统）
   
   使用 CSS 变量实现主题切换，避免重复样式。
   
   ## 影响范围
   
   需要更新所有页面的样式，工作量较大。

这个 Issue 不仅提出了需求，还提供了实现建议，维护者更容易评估。

**Issue 模板**

GitHub 支持 Issue 模板，规范化 Issue 内容。在仓库创建 ``.github/ISSUE_TEMPLATE/`` 目录，添加模板文件：

- ``bug_report.md``：Bug 报告模板
- ``feature_request.md``：功能建议模板
- ``custom.md``：自定义模板

创建 Issue 时，GitHub 会提示选择模板，模板内容自动填充到 Issue 描述框。

一个 Bug 报告模板示例：

::

   ---
   name: Bug report
   about: Report a bug
   ---
   
   ## Bug 描述
   
   [简要描述问题]
   
   ## 复现步骤
   
   1. [步骤 1]
   2. [步骤 2]
   3. [步骤 3]
   
   ## 预期行为
   
   [应该发生什么]
   
   ## 实际行为
   
   [实际发生了什么]
   
   ## 环境
   
   - 操作系统：[如 macOS 12.0]
   - 浏览器：[如 Chrome 108]
   - 版本：[如 v2.1.0]
   
   ## 日志/截图
   
   [如有]

使用模板确保每个 Issue 都包含必要信息，减少无效 Issue。

Issue 的管理
------------

项目可能有大量 Issue，需要有效管理。

**标签分类**

标签帮助分类 Issue。GitHub 默认提供一些标签：

- ``bug``：Bug 报告
- ``documentation``：文档相关
- ``enhancement``：功能增强
- ``good first issue``：适合新手
- ``help wanted``：需要帮助

可以根据项目需求创建自定义标签：

- 类型：feature、bug、refactor、docs
- 优先级：priority-high、priority-medium、priority-low
- 状态：in-progress、blocked、ready-for-review
- 范围：frontend、backend、testing、security

标签使用原则：

- 每个 Issue 至少一个标签
- 标签名称清晰，颜色区分明显
- 标签数量适中，太多会难以选择

**里程碑追踪**

里程碑标记阶段性目标。比如 "v1.0 Release"、"Q1 Tasks"。

创建里程碑：Issue 页面 → "Milestones" → "New milestone"。填写标题、描述、截止日期。

把 Issue 添加到里程碑：Issue 页面右侧 "Milestone" 选择框。

里程碑的作用：

- 规划目标：把 v1.0 要完成的 Issue 添加到里程碑
- 追踪进度：里程碑显示完成百分比
- 激励团队：明确的截止日期增加紧迫感

**Issue 分配**

Issue 可以分配给团队成员。Issue 页面右侧 "Assignees" 选择框。

分配原则：

- Bug 报告分配给相关模块的负责人
- 功能建议分配给负责开发的成员
- 不确定的 Issue 先不分配，讨论后再分配

**Issue 关闭**

Issue 有两种状态：Open（待处理）和 Closed（已处理）。

关闭 Issue 的情况：

- Bug 已修复（提交 PR 时写 "Fixes #123"，PR 合并后 Issue 自动关闭）
- 功能已实现
- Issue 无效（重复报告、无法复现）
- 功能建议被拒绝

关闭 Issue 时可以添加评论，说明关闭原因。

Issue 与代码的关联
------------------

Issue 可以关联 PR、提交、其他 Issue。

**自动关闭 Issue**

PR 合并时自动关闭 Issue：

::

   PR 描述中写：
   Fixes #123
   
   PR 合并后，Issue #123 自动关闭。

其他格式：

- ``Fixes #123`` 或 ``Closes #123``：合并后关闭 Issue
- ``Related to #123``：关联但不关闭

这个功能让 Issue 与代码改动关联，方便追踪。

**Issue 引用**

在 Issue 或 PR 中引用其他 Issue：

::

   Related to #456, we need to handle the case when...

点击 Issue 编号（如 #123）会跳转到对应 Issue。这方便跨 Issue 讨论。

**代码链接**

在 Issue 中引用代码片段：

::

   This bug is caused by the code at:
   
   https://github.com/owner/project/blob/main/src/auth.py#L45

GitHub 会显示代码片段，帮助定位问题。

Issue 的讨论
------------

Issue 不只是问题记录，也是讨论平台。

**评论交流**

Issue 页面下方有评论框，可以发表意见：

- 维护者可以回应问题
- 用户可以补充信息
- 开发者可以讨论方案

评论会通知相关人员，形成对话。

**投票功能**

GitHub 支持 Issue 投票（使用表情反应）：

- 👍：支持这个功能建议
- 👎：反对这个功能建议
- 🎉：庆祝 Issue 解决

投票帮助维护者判断 Issue 的重要性。功能建议收到很多 👍，说明用户需求强烈。

**避免无效讨论**

Issue 讨论应该聚焦问题，避免：

- 偏离主题的讨论（另开 Issue）
- 情绪化争论（保持友善）
- 重复信息（精简表达）

如果讨论过长，维护者可以总结结论，关闭讨论。

Issue 的最佳实践
----------------

**先搜索再创建**

创建 Issue 前先搜索是否已有类似 Issue：

- 搜索关键词
- 查看标签分类
- 检查 Closed Issue

如果已有相同 Issue，不要重复创建。可以在已有 Issue 下补充信息。

**标题简洁明确**

标题应该概括 Issue 内容：

- 差："登录有问题"
- 好："登录失败，密码包含特殊字符时报错"

好的标题让人一眼了解问题。

**描述详细但不冗余**

描述应该包含必要信息，但不啰嗦：

- Bug 报告：复现步骤最重要
- 功能建议：背景和建议最重要

不要写无关信息（如个人故事）。

**及时回应**

创建 Issue 后，关注维护者的回应：

- 维护者可能要求更多信息，及时补充
- 维护者可能提出方案，参与讨论

长时间不回应的 Issue 可能被关闭。

**尊重维护者**

维护者可能拒绝你的 Issue。不要抱怨：

- Bug 无法复现：可能需要更多信息
- 功能建议被拒绝：可能不符合项目方向

感谢维护者的时间，继续寻找其他贡献机会。

用 Issue 驱动项目进展
---------------------

Issue 不仅是问题记录，还可以驱动项目进展。

**Issue 作为任务清单**

团队可以把 Issue 作为任务清单：

- 每个开发任务创建 Issue
- Issue 分配给开发者
- 完成任务后关闭 Issue

这种方式让任务透明，进度可见。

**Issue 作为规划工具**

里程碑和标签帮助规划：

- 把 v1.0 的 Issue 添加到 "v1.0 Release" 里程碑
- 高优先级 Issue 标记 "priority-high"
- 新手任务标记 "good first issue"

Issue 成了项目规划的载体。

**Issue 作为沟通中心**

Issue 讨论功能让团队协作：

- 讨论设计方案
- 分享技术问题
- 协调开发进度

公开的 Issue 让所有人参与，透明协作。

总结
----

本章我们学习了协作开发的三个方面：

1. 团队管理：组织协作、权限分配、项目管理工具
2. Fork 与贡献：开源贡献流程、Fork 同步、合并冲突
3. Issue 跟踪：有效 Issue、Issue 管理、Issue 与代码关联

这三者构成完整的协作体系：内部团队管理、外部开源贡献、问题跟踪讨论。

下一章我们会学习高级技巧——GitHub CLI、GitHub API、安全最佳实践，让协作更高效。