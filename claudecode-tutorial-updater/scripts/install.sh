#!/bin/bash
# Claude Code教程自动更新技能安装脚本

set -e

echo "🚀 开始安装 claudecode-tutorial-updater 技能..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$PYTHON_VERSION < 3.9" | bc -l) )); then
    echo "❌ 错误: Python版本需要 >= 3.9，当前版本: $PYTHON_VERSION"
    exit 1
fi

# 获取安装路径
SKILL_DIR="$HOME/.claude/skills/claudecode-tutorial-updater"
echo "📂 安装路径: $SKILL_DIR"

# 创建目录
mkdir -p "$SKILL_DIR"

# 复制文件
echo "📦 复制技能文件..."
cp -r ./* "$SKILL_DIR/"

# 安装依赖
echo "📦 安装Python依赖..."
pip3 install requests beautifulsoup4 pyyaml > /dev/null 2>&1

# 设置执行权限
chmod +x "$SKILL_DIR/src/"*.py
chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true

# 添加cron定时任务
echo "⏰ 配置每日自动检查任务..."
CRON_JOB="0 2 * * * cd $SKILL_DIR/src && python3 checker.py > /var/log/claudecode-updater.log 2>&1"

# 检查是否已存在
(crontab -l 2>/dev/null || true) | grep -v "claudecode-updater" | { cat; echo "$CRON_JOB"; } | crontab -

echo "✅ Cron定时任务已配置，每天凌晨2点自动检查更新"

# 配置提示
echo ""
echo "⚙️  请配置 config/config.yaml："
echo "1. 设置教程仓库路径 repo_path"
echo "2. 配置飞书webhook（可选，用于接收通知）"
echo "3. 根据需要调整检查频率和告警阈值"

echo ""
echo "🎉 安装完成！"
echo ""
echo "📖 使用命令："
echo "  /claudecode-update check          # 手动检查更新"
echo "  /claudecode-update force-update   # 强制更新教程"
echo "  /claudecode-update history        # 查看更新历史"
echo "  /claudecode-update version        # 查看版本信息"
echo ""
echo "📝 配置文件路径: $SKILL_DIR/config/config.yaml"
