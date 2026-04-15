# claudecode-tutorial-updater

Claude Code教程自动更新维护技能，自动追踪官方变更，持续更新教程内容。

## ✨ 功能特性

- 🔍 **多渠道监测**：官方文档、GitHub仓库、发布公告、插件市场、社区动态
- ⚡ **智能分析**：自动识别变更类型、优先级、影响范围
- 📊 **详细报告**：生成变更报告和更新建议
- 🚨 **实时告警**：飞书/邮件通知重要变更
- 🔄 **自动更新**：批量更新教程内容、代码示例、文档
- 📅 **版本管理**：自动备份、提交、推送更新
- ⏰ **定时任务**：每日自动检查，也可手动触发

## 📦 安装方法

### 一键安装
```bash
git clone https://github.com/your-repo/claudecode-tutorial-updater.git
cd claudecode-tutorial-updater
chmod +x scripts/install.sh
./scripts/install.sh
```

### 手动安装
1. 复制整个目录到 `~/.claude/skills/claudecode-tutorial-updater/`
2. 安装依赖：`pip3 install requests beautifulsoup4 pyyaml`
3. 配置 `config/config.yaml`
4. 添加cron定时任务：`0 2 * * * cd ~/.claude/skills/claudecode-tutorial-updater/src && python3 checker.py`

## ⚙️ 配置说明

编辑 `config/config.yaml`：

```yaml
check:
  # 检查频率：daily/6hourly/hourly
  frequency: "daily"
  # 执行时间（cron表达式）
  schedule: "0 2 * * *"

notify:
  # 通知方式：feishu/email
  channels: ["feishu"]
  # 飞书webhook
  feishu_webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  # 告警阈值：critical/major/minor
  alert_threshold: "major"

update:
  # 教程仓库路径
  repo_path: "/workspace/projects/claudecode-book"
  # 自动提交到GitHub
  auto_commit: true
  # 自动推送到远程
  auto_push: false
```

## 🚀 使用方法

### 命令行命令
```bash
# 手动检查更新
/claudecode-update check

# 强制更新到最新版本
/claudecode-update force-update

# 查看更新历史
/claudecode-update history

# 查看版本信息
/claudecode-update version
```

### 手动执行脚本
```bash
# 检查更新
python3 src/checker.py

# 分析变更并生成报告
python3 src/analyzer.py

# 发送测试通知
python3 src/notifier.py
```

## 📊 变更优先级

| 优先级 | 说明 | 响应时间 | 通知级别 |
|-------|------|---------|---------|
| 🔴 critical | 大版本发布、核心功能变更、API不兼容更新、安全更新 | 24小时内 | 必通知 |
| 🟡 major | 新插件发布、新模型发布、重要功能升级 | 72小时内 | 必通知 |
| 🟢 minor | 文档更新、小功能优化、Bug修复 | 1周内 | 可选通知 |

## 📁 目录结构

```
claudecode-tutorial-updater/
├── SKILL.md                    # 技能描述
├── skill.json                  # 技能元数据
├── src/
│   ├── checker.py              # 官方更新检查器
│   ├── analyzer.py             # 变更分析器
│   ├── updater.py              # 内容更新器
│   └── notifier.py             # 通知告警器
├── commands/                   # Claude Code命令
│   ├── check.md
│   ├── force-update.md
│   ├── history.md
│   └── version.md
├── config/
│   └── config.yaml             # 配置文件
├── scripts/
│   ├── install.sh              # 安装脚本
│   └── uninstall.sh            # 卸载脚本
├── state/                      # 状态存储（自动生成）
│   └── last_check.json
└── README.md                   # 使用说明
```

## 🔒 权限说明

需要以下权限：
- `file:read` / `file:write` - 读写教程文件
- `git:read` / `git:write` - Git操作
- `http:fetch` - 访问官方渠道获取更新

## 📝 更新流程

1. **定时触发**：每日凌晨2点自动执行检查
2. **变更检测**：扫描所有官方渠道，对比内容哈希
3. **变更分析**：分析变更类型、优先级、影响范围
4. **告警通知**：通过飞书发送变更报告
5. **内容更新**：用户确认后自动更新相关章节
6. **版本提交**：自动提交并推送更新到GitHub
7. **完成通知**：发送更新完成通知

## 🤝 贡献

欢迎提交Issue和PR，共同完善这个自动更新技能！

## 📄 许可证

MIT License
