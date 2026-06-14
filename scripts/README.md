# fuxi 脚本

`fuxi.py` 负责机械工作，不负责替代 AI 的语义判断。

## 前置条件

安装 Python 3.10 或更高版本。

当前机器上的 Windows 应用执行别名 `python.exe` 无法正常启动，因此运行前需要安装正式 Python，或修复系统的 Python 命令。

## 命令

初始化：

```powershell
python .\scripts\fuxi.py init
```

入库一个文件：

```powershell
python .\scripts\fuxi.py ingest "D:\资料\文章.md"
```

入库一个文件夹：

```powershell
python .\scripts\fuxi.py ingest "D:\资料"
```

记录一句话灵感：

```powershell
python .\scripts\fuxi.py idea "研究 AI Agent 的记忆机制"
```

记录任务：

```powershell
python .\scripts\fuxi.py idea "整理项目验收清单" --type task_note
```

重建索引和关联：

```powershell
python .\scripts\fuxi.py index
python .\scripts\fuxi.py related
python .\scripts\fuxi.py topics
```

检索主题页、笔记、复习和选题：

```powershell
python .\scripts\fuxi.py search "Agent 记忆"
python .\scripts\fuxi.py search "Codex" --limit 5
```

生成待复习知识点列表：

```powershell
python .\scripts\fuxi.py review-list
```

检查所有笔记的 frontmatter：

```powershell
python .\scripts\fuxi.py validate
```

运行完整冒烟测试：

```powershell
python .\scripts\smoke_test.py
```

## 能力边界

- 脚本负责复制原文、生成模板、索引、规则关联、主题导航、检索和复习排序。
- 摘要、标签、知识点识别、主题综合判断等语义工作仍由 AI 按 `AGENTS.md` 完成。
- `topics` 只更新 `wiki/_自动主题索引.md`，不会覆盖 AI 编写的主题页。
