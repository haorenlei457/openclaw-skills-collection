---
name: "claudecode-update history"
description: "查看更新历史记录"
---

查看最近的更新历史：

```bash
cd {{config.update.repo_path}}
git log --pretty=format:"%h %ad %s" --date=format:"%Y-%m-%d %H:%M" -20 | grep -E "(sync|update|docs)" | head -20
```

**最近20条更新记录：**
{{output}}
