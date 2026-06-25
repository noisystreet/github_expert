# agents.md — GitHub 专家指南项目

## 项目概述

本项目编写一本 **GitHub 专家指南** 技术文档，使用 reStructuredText（`.rst`）格式，基于 Sphinx 构建。

- 文档源目录：`source/`
- 构建输出：`./_build/html/`（`make html` 后生成）
- 目标读者：从初学者到进阶用户，希望系统学习 GitHub 的开发者
- 参考资料：GitHub 官方文档、Git 官方文档、社区最佳实践
- 平台：跨平台（Windows、macOS、Linux）

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `source/preface/index.rst` | 前言：编写动机、目标读者、如何阅读本书 |
| `source/index.rst` | Sphinx 根文档（toctree 入口） |
| `source/chapter_01_basics/` | GitHub 基础入门（什么是 GitHub、账户设置、基本概念） |
| `source/chapter_02_repo/` | 仓库管理（创建仓库、仓库设置、分支管理） |
| `source/chapter_03_workflow/` | 工作流（Pull Request、代码审查、CI/CD） |
| `source/chapter_04_collaboration/` | 协作开发（团队管理、Fork 与贡献、Issue 跟踪） |
| `source/chapter_05_advanced/` | 高级技巧（GitHub CLI、GitHub API、安全最佳实践） |
| `source/appendix/` | 附录（参考资源、术语表） |
| `examples/` | 可运行的 Python 示例代码 |
| `source/conf.py` | Sphinx 构建配置 |
| `Makefile` | 构建入口（`make html` / `make clean`） |
| `scripts/precommit-check.sh` | 预提交检查脚本（验证 RST 文档语法） |
| `requirements.txt` | 构建依赖（sphinx, sphinx-rtd-theme, sphinxcontrib-mermaid） |
| `.readthedocs.yaml` | Read the Docs 构建配置 |
| `LICENSE` | CC BY-SA 4.0 许可证 |
| `.gitignore` | 版本控制忽略规则 |
| `agents.md` | **本文件**：AI 助手的工作上下文和约束 |

## 通用约束

1. **许可证**：本文档采用 CC BY-SA 4.0（Creative Commons Attribution-ShareAlike 4.0 International），详见 `LICENSE` 文件
2. **文档格式**：使用 reStructuredText（`.rst`）格式，中文写作
3. **git hooks**：clone 后首次提交前，运行以下命令启用 pre-commit 检查：

   ```bash
   git config --local core.hooksPath .githooks
   ```

   否则 pre-commit 检查不会自动生效。
4. **引用源码**：使用绝对路径的 `file:///` 链接引用源码文件，格式为 `` `链接文本 <file:///绝对路径/文件>`__ ``
5. **避免冗余**：不创建不必要的文件，优先编辑已有文件
6. **权限**：不做 `git push --force`、`reset --hard` 等破坏性操作
7. **代码示例**：在文档中引用代码时，说明其所属文件和行号范围
8. **示例验证**：所有 `.py` 示例代码应保证可运行

## 文档写作规范

### 文档结构
- 每篇文档应有标题
- 按章节组织，章节层级不超过三级
- 内容末尾标注生成日期和项目名称

### 引用规范
- 引用外部文档使用标准 RST 链接语法
- 引用命令或代码使用 `` `` `` 反引号标记
- 关键命令应提供可执行的代码块

### 内容深度
- 概念讲解与实际操作相结合
- 复杂流程配合 Mermaid 图表说明
- 关键配置用表格列出参数说明
- 避免大段堆叠代码，优先提炼核心模式

### 写作风格（核心：浅入深出，夹叙夹议）

**禁止罗列结论**。每一个知识点都必须有推导过程，遵循"是什么 → 为什么 → 怎么用 → 最佳实践"的递进链条。

- **浅入深出**：从直观可操作的场景出发引入概念，读者能"看见"它在做什么，再逐步深入高级用法。每一节都遵循：实际问题 → 基本操作 → 引出进阶技巧 → 最佳实践。**不要一上来就甩概念定义。**
- **夹叙夹议**：叙述"GitHub 提供什么功能"的同时，必须穿插"为什么这样设计"——团队协作考量、安全因素、与其他方案的对比。功能是手段，不是目的。
- **避免知识点罗列**：每个新概念必须有上下文铺垫才引入。如果出现"XX有以下几个特点：1... 2... 3..."这种列表体，必须有前置案例让读者自然感受到这些特点的存在，而不是突兀地堆砌。
- **实践即证据**：每一个论断必须附实际操作截图或命令示例佐证。没有实际操作支撑的观点都是空谈。关键操作要标注具体的 GitHub 界面位置或命令行参数。
- **过渡自然**：段落之间、章节之间要有承上启下的过渡句。比如"上一节我们掌握了创建仓库，但要高效协作还需要分支管理，接下来我们深入分支策略"。禁止生硬切换话题。

## 写作路线图

按以下顺序推进内容编写：

1. **第 1 章：GitHub 基础入门** — GitHub 是什么、账户设置、基本概念
2. **第 2 章：仓库管理** — 创建仓库、仓库设置、分支管理策略
3. **第 3 章：工作流** — Pull Request、代码审查、CI/CD 集成
4. **第 4 章：协作开发** — 团队管理、Fork 与贡献、Issue 跟踪
5. **第 5 章：高级技巧** — GitHub CLI、GitHub API、安全最佳实践
6. **附录** — 参考资源、术语表

## 构建方法

```bash
# 安装依赖
pip install -r requirements.txt

# 构建 HTML 文档
make html

# 本地预览（默认 8000 端口）
make serve

# 清理构建
make clean
```

## 内容更新规范

1. 新增章节时，在 `source/index.rst` 中添加 toctree 条目
2. 每个章节目录下创建 `index.rst` 作为章节入口
3. 代码示例放在 `examples/` 目录，并在文档中引用
4. 图片资源放在 `source/_static/images/` 目录
5. 保持章节之间的逻辑连贯性