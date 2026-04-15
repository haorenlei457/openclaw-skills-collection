---
name: "claudecode-update version"
description: "查看当前教程和技能版本信息"
---

查看版本信息：

```python
{{python}}
import os
import json
import subprocess

# 读取技能版本
skill_json_path = os.path.join(os.path.dirname(__file__), '../skill.json')
with open(skill_json_path, 'r') as f:
    skill_info = json.load(f)

# 读取教程版本
repo_path = os.path.join(os.path.dirname(__file__), '../../../../claudecode-book')
try:
    result = subprocess.run(
        ['git', 'log', '-1', '--pretty=format:%h %ad %s'],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    tutorial_version = result.stdout.strip()
except:
    tutorial_version = "未知"

print("## 📊 版本信息")
print("")
print(f"### 自动更新技能版本")
print(f"- 名称: {skill_info['name']}")
print(f"- 版本: {skill_info['version']}")
print(f"- 描述: {skill_info['description']}")
print("")
print(f"### Claude Code教程版本")
print(f"- 最新提交: {tutorial_version}")
print(f"- 仓库路径: {repo_path}")
```
