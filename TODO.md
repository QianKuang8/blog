# TODO

## 创建私有原文归档仓库 `blog-sources`

2026-10-10 整理时，外部文章全文（70 篇）和 NotebookLM 历史摘要（24 份）已从本仓库移出，`sources/orig/` 只保留元信息。当时的会话没有权限创建或推送 GitHub 仓库，以下步骤需要手动完成。

1. 在 GitHub 新建空的**私有**仓库 `QianKuang8/blog-sources`，不要勾选初始化 README。
2. 导入内容，任选一种：
   - **使用会话提供的 `blog-sources.bundle`**（已含 README）：

     ```bash
     git clone blog-sources.bundle blog-sources
     cd blog-sources
     git remote set-url origin https://github.com/QianKuang8/blog-sources.git
     git push -u origin main
     ```

   - **没有 bundle 时，从本仓库历史重建**（提交 `bd38d9b` 仍保留全部全文，结果与 bundle 相同）：

     ```bash
     mkdir blog-sources && cd blog-sources && git init -b main
     git -C /path/to/blog archive bd38d9b sources/orig sources/nlm | tar -x --strip-components=1
     rm orig/a-philosophy-of-software-design.md  # 书籍证据记录继续留在公开仓库
     # 按 WORKFLOW.md 的“原文归档”一节补一份 README.md，然后提交并推送到上面的私有仓库
     ```

3. 在博客仓库根目录克隆到被忽略的 `sources/archive/`：

   ```bash
   git clone https://github.com/QianKuang8/blog-sources.git sources/archive
   ```

4. 完成后删除本文件，并删掉 AGENTS.md 中指向它的说明。

## 可选：从公开仓库历史中清除全文

全文仍存在于本仓库 `bd38d9b` 及更早的 git 历史中。若要彻底清除，需要用 `git filter-repo` 等工具改写 `main` 的历史并强制推送；这会改变所有提交哈希，已有的克隆需要重新拉取。完成上面的私有仓库迁移之后再决定是否执行。
