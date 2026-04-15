#!/usr/bin/env python3
"""
变更分析器 - 分析官方变更的类型、优先级和更新建议
"""

import json
import yaml
from datetime import datetime

class ChangeAnalyzer:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # 变更类型优先级映射
        self.priority_map = {
            'release': 'critical',
            'new_feature': 'critical',
            'breaking_change': 'critical',
            'security_update': 'critical',
            'new_plugin': 'major',
            'model_update': 'major',
            'api_change': 'major',
            'code_update': 'minor',
            'doc_update': 'minor',
            'plugin_update': 'minor'
        }
        
        # 变更影响的章节映射
        self.impacted_chapters = {
            'release': ['所有章节'],
            'new_feature': ['新增章节'],
            'breaking_change': ['核心模块', 'API示例'],
            'security_update': ['第12章 - 安全机制'],
            'new_plugin': ['第13章 - 官方插件详解'],
            'model_update': ['第14章 - 大模型选择与配置指南'],
            'api_change': ['所有代码示例章节', 'API参考'],
            'code_update': ['相关功能模块'],
            'doc_update': ['相关文档章节'],
            'plugin_update': ['第13章 - 官方插件详解']
        }
    
    def analyze_change(self, change):
        """分析单个变更"""
        change_type = change['type']
        priority = self.priority_map.get(change_type, 'minor')
        impacted_chapters = self.impacted_chapters.get(change_type, ['相关章节'])
        
        # 计算预计更新时间
        estimated_hours = self._calculate_estimated_hours(priority)
        
        # 生成更新建议
        update_suggestions = self._generate_update_suggestions(change_type, change)
        
        return {
            **change,
            'priority': priority,
            'impacted_chapters': impacted_chapters,
            'estimated_hours': estimated_hours,
            'update_suggestions': update_suggestions,
            'response_deadline': self._calculate_deadline(priority)
        }
    
    def _calculate_estimated_hours(self, priority):
        """计算预计更新时间"""
        if priority == 'critical':
            return 8
        elif priority == 'major':
            return 4
        else:  # minor
            return 2
    
    def _calculate_deadline(self, priority):
        """计算响应截止时间"""
        hours = self.config['priority'].get(priority, 168)
        return f"{hours}小时内"
    
    def _generate_update_suggestions(self, change_type, change):
        """生成更新建议"""
        suggestions = []
        
        if change_type == 'new_plugin':
            suggestions.extend([
                "1. 阅读新插件的官方文档",
                "2. 测试插件的功能和使用方法",
                "3. 在第13章添加新插件的详细说明",
                "4. 添加使用示例和最佳实践",
                "5. 更新插件选择指南"
            ])
        elif change_type == 'model_update':
            suggestions.extend([
                "1. 获取新模型的性能参数、价格信息",
                "2. 进行性能测试对比",
                "3. 更新第14章的对比表格",
                "4. 添加新模型的适用场景推荐",
                "5. 更新选择流程图"
            ])
        elif change_type == 'release':
            suggestions.extend([
                "1. 阅读版本发布公告，理解所有变更",
                "2. 测试新功能的使用方法",
                "3. 评估对现有教程内容的影响",
                "4. 制定更新计划",
                "5. 更新相关章节和示例"
            ])
        elif change_type == 'breaking_change':
            suggestions.extend([
                "1. 分析不兼容变更的影响范围",
                "2. 搜索所有相关代码示例",
                "3. 批量更新过时的代码示例",
                "4. 更新常见问题排查内容",
                "5. 添加升级迁移指南"
            ])
        elif change_type == 'api_change':
            suggestions.extend([
                "1. 对比API接口变化",
                "2. 更新所有相关的代码示例",
                "3. 更新API参考文档",
                "4. 添加变更说明和迁移指南",
                "5. 更新FAQ内容"
            ])
        elif change_type == 'doc_update':
            suggestions.extend([
                "1. 对比官方文档变更内容",
                "2. 同步更新教程中对应的部分",
                "3. 补充新的说明和示例",
                "4. 更新最佳实践内容"
            ])
        else:
            suggestions.extend([
                "1. 评估变更对教程的影响",
                "2. 更新相关章节内容",
                "3. 测试更新后的内容正确性"
            ])
        
        return suggestions
    
    def analyze_changes(self, changes):
        """批量分析变更"""
        analyzed_changes = []
        for change in changes:
            analyzed_changes.append(self.analyze_change(change))
        
        # 按优先级排序
        priority_order = {'critical': 0, 'major': 1, 'minor': 2}
        analyzed_changes.sort(key=lambda x: priority_order[x['priority']])
        
        return analyzed_changes
    
    def generate_report(self, analyzed_changes):
        """生成变更报告"""
        if not analyzed_changes:
            return "✅ 未发现新的变更"
        
        report = []
        report.append("## 📊 Claude Code官方变更报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"发现变更数: {len(analyzed_changes)}")
        report.append("")
        
        # 按优先级分组
        critical = [c for c in analyzed_changes if c['priority'] == 'critical']
        major = [c for c in analyzed_changes if c['priority'] == 'major']
        minor = [c for c in analyzed_changes if c['priority'] == 'minor']
        
        if critical:
            report.append("### 🔴 紧急变更 (需要24小时内处理)")
            for change in critical:
                report.append(f"#### {change['title']}")
                report.append(f"- 来源: {change['source']}")
                report.append(f"- 链接: {change['url']}")
                report.append(f"- 影响章节: {', '.join(change['impacted_chapters'])}")
                report.append(f"- 预计更新时间: {change['estimated_hours']}小时")
                report.append("**更新建议:**")
                for suggestion in change['update_suggestions']:
                    report.append(f"  {suggestion}")
                report.append("")
        
        if major:
            report.append("### 🟡 重要变更 (需要72小时内处理)")
            for change in major:
                report.append(f"#### {change['title']}")
                report.append(f"- 来源: {change['source']}")
                report.append(f"- 链接: {change['url']}")
                report.append(f"- 影响章节: {', '.join(change['impacted_chapters'])}")
                report.append(f"- 预计更新时间: {change['estimated_hours']}小时")
                report.append("**更新建议:**")
                for suggestion in change['update_suggestions']:
                    report.append(f"  {suggestion}")
                report.append("")
        
        if minor:
            report.append("### 🟢 一般变更 (需要1周内处理)")
            for change in minor:
                report.append(f"#### {change['title']}")
                report.append(f"- 来源: {change['source']}")
                report.append(f"- 链接: {change['url']}")
                report.append(f"- 预计更新时间: {change['estimated_hours']}小时")
                report.append("")
        
        report.append("---")
        report.append("**处理建议:** 请根据优先级依次处理变更，处理完成后标记为已完成。")
        
        return '\n'.join(report)

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(__file__))
    from checker import UpdateChecker
    
    checker = UpdateChecker()
    changes = checker.check_all()
    
    if changes:
        analyzer = ChangeAnalyzer()
        analyzed = analyzer.analyze_changes(changes)
        report = analyzer.generate_report(analyzed)
        print(report)
    else:
        print("✅ 未发现新的变更")
