---
name: "claudecode-update check"
description: "手动检查Claude Code官方更新"
---

执行Claude Code官方更新检查：

```python
{{python}}
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from checker import UpdateChecker
from analyzer import ChangeAnalyzer
from notifier import Notifier

# 执行检查
checker = UpdateChecker()
changes = checker.check_all()

if not changes:
    print("✅ 未发现新的官方变更")
else:
    # 分析变更
    analyzer = ChangeAnalyzer()
    analyzed_changes = analyzer.analyze_changes(changes)
    report = analyzer.generate_report(analyzed_changes)
    
    print(report)
    
    # 发送通知
    notifier = Notifier()
    notifier.send_change_report(report, analyzed_changes)
```
