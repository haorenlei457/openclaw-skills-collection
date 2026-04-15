#!/usr/bin/env python3
"""
通知器 - 发送变更告警和报告
"""

import os
import json
import yaml
import requests
from datetime import datetime

class Notifier:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.notify_channels = self.config['notify']['channels']
        self.alert_threshold = self.config['notify']['alert_threshold']
        self.feishu_webhook = self.config['notify'].get('feishu_webhook', '')
        
        # 优先级权重
        self.priority_weight = {
            'critical': 0,
            'major': 1,
            'minor': 2
        }
    
    def _should_alert(self, priority):
        """判断是否需要告警"""
        return self.priority_weight[priority] <= self.priority_weight[self.alert_threshold]
    
    def send_feishu_message(self, content):
        """发送飞书消息"""
        if not self.feishu_webhook:
            return False, "飞书webhook未配置"
        
        try:
            headers = {'Content-Type': 'application/json'}
            data = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "📊 Claude Code官方更新提醒"
                        },
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": content
                        },
                        {
                            "tag": "hr"
                        },
                        {
                            "tag": "note",
                            "elements": [
                                {
                                    "tag": "plain_text",
                                    "content": f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                }
                            ]
                        }
                    ]
                }
            }
            
            response = requests.post(
                self.feishu_webhook,
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )
            response.raise_for_status()
            return True, "飞书消息发送成功"
        except Exception as e:
            return False, f"飞书消息发送失败: {e}"
    
    def send_email(self, subject, content):
        """发送邮件通知（待实现）"""
        # 可以根据需要实现SMTP邮件发送
        return False, "邮件通知功能待实现"
    
    def send_notification(self, content, priority='minor'):
        """发送通知"""
        if not self._should_alert(priority):
            return True, "优先级低于告警阈值，跳过通知"
        
        results = []
        
        for channel in self.notify_channels:
            if channel == 'feishu':
                success, msg = self.send_feishu_message(content)
                results.append(msg)
            elif channel == 'email':
                success, msg = self.send_email("Claude Code官方更新提醒", content)
                results.append(msg)
            else:
                results.append(f"未知通知渠道: {channel}")
        
        return all(["成功" in res for res in results]), '\n'.join(results)
    
    def send_change_report(self, report, analyzed_changes):
        """发送变更报告"""
        if not analyzed_changes:
            return True, "没有变更需要通知"
        
        # 确定最高优先级
        max_priority = max(
            [c['priority'] for c in analyzed_changes],
            key=lambda x: self.priority_weight[x]
        )
        
        # 简化报告内容适合飞书显示
        simplified_report = self._simplify_report_for_feishu(report, analyzed_changes)
        return self.send_notification(simplified_report, max_priority)
    
    def _simplify_report_for_feishu(self, full_report, analyzed_changes):
        """简化报告内容适合飞书显示"""
        report = []
        
        # 统计
        critical_count = len([c for c in analyzed_changes if c['priority'] == 'critical'])
        major_count = len([c for c in analyzed_changes if c['priority'] == 'major'])
        minor_count = len([c for c in analyzed_changes if c['priority'] == 'minor'])
        
        report.append("## 📊 Claude Code官方变更通知")
        report.append("")
        report.append(f"**发现变更总数: {len(analyzed_changes)}**")
        report.append(f"- 🔴 紧急变更: {critical_count}个")
        report.append(f"- 🟡 重要变更: {major_count}个")
        report.append(f"- 🟢 一般变更: {minor_count}个")
        report.append("")
        
        # 紧急变更
        if critical_count > 0:
            report.append("### 🔴 紧急变更（24小时内处理）")
            for change in [c for c in analyzed_changes if c['priority'] == 'critical']:
                report.append(f"**{change['title']}**")
                report.append(f"- 来源: {change['source']}")
                report.append(f"- 影响章节: {', '.join(change['impacted_chapters'])}")
                report.append(f"- [查看详情]({change['url']})")
                report.append("")
        
        # 重要变更
        if major_count > 0:
            report.append("### 🟡 重要变更（72小时内处理）")
            for change in [c for c in analyzed_changes if c['priority'] == 'major']:
                report.append(f"**{change['title']}**")
                report.append(f"- 来源: {change['source']}")
                report.append(f"- 影响章节: {', '.join(change['impacted_chapters'])}")
                report.append(f"- [查看详情]({change['url']})")
                report.append("")
        
        # 一般变更
        if minor_count > 0:
            report.append("### 🟢 一般变更（1周内处理）")
            report.append(f"共 {minor_count} 个一般变更，详情请查看完整报告。")
            report.append("")
        
        report.append("---")
        report.append("**请及时处理上述变更，确保教程内容与官方最新版本保持一致。**")
        
        return '\n'.join(report)
    
    def send_update_complete_notification(self, update_results):
        """发送更新完成通知"""
        content = []
        content.append("## ✅ Claude Code教程更新完成")
        content.append("")
        content.append("更新结果:")
        for result in update_results:
            content.append(f"- {result}")
        content.append("")
        content.append("教程已同步到最新官方版本！")
        
        return self.send_notification('\n'.join(content), 'major')

if __name__ == "__main__":
    # 测试通知
    notifier = Notifier()
    test_content = "这是一条测试通知，用于验证通知功能是否正常工作。"
    success, msg = notifier.send_notification(test_content, 'minor')
    print(msg)
