---
name: "claudecode-update force-update"
description: "强制更新教程到最新官方版本"
---

强制执行教程内容更新：

```python
{{python}}
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from checker import UpdateChecker
from analyzer import ChangeAnalyzer
from updater import TutorialUpdater
from notifier import Notifier

# 执行检查
checker = UpdateChecker()
changes = checker.check_all()

if not changes:
    print("✅ 未发现新的变更，无需更新")
else:
    # 分析变更
    analyzer = ChangeAnalyzer()
    analyzed_changes = analyzer.analyze_changes(changes)
    report = analyzer.generate_report(analyzed_changes)
    
    print("### 发现以下变更，开始更新:")
    print(report)
    
    # 执行更新（这里需要根据实际变更内容生成更新操作）
    updater = TutorialUpdater()
    update_results = []
    
    # 备份
    success, msg = updater.backup_tutorial()
    update_results.append(msg)
    print(msg)
    
    if success:
        # 拉取最新代码
        success, msg = updater.pull_latest()
        update_results.append(msg)
        print(msg)
        
        # 这里根据具体变更内容执行相应的更新操作
        # 示例：假设需要更新某个章节
        # update_op = {
        #     'type': 'update_chapter',
        #     'file': '13-official-plugins.md',
        #     'content': '新内容...'
        # }
        # success, msg = updater.run_update(analyzed_changes[0], [update_op])
        # update_results.extend(msg)
        
        # 发送更新完成通知
        notifier = Notifier()
        notifier.send_update_complete_notification(update_results)
        
        print("\n✅ 更新流程执行完成，请检查更新内容是否正确。")
```
