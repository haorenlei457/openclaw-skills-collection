#!/bin/bash
# Claude Code教程自动更新技能卸载脚本

echo "⚠️  开始卸载 claudecode-tutorial-updater 技能..."

# 卸载cron任务
echo "⏰ 移除定时任务..."
(crontab -l 2>/dev/null || true) | grep -v "claudecode-updater" | crontab -

# 删除技能文件
SKILL_DIR="$HOME/.claude/skills/claudecode-tutorial-updater"
if [ -d "$SKILL_DIR" ]; then
    echo "🗑️  删除技能文件..."
    rm -rf "$SKILL_DIR"
fi

# 删除日志
sudo rm -f /var/log/claudecode-updater.log > /dev/null 2>&1 || true

echo "✅ 卸载完成！"
