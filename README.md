# OpenClaw 技能集合

本仓库用于收集和管理各类 OpenClaw 自定义技能。

## 技能列表

### 📌 claudecode-tutorial-updater
ClaudeCode 教程自动更新技能，用于自动检测、更新和通知 ClaudeCode 官方教程的变更。

**功能特性：**
- 自动检测 ClaudeCode 官方教程更新
- 智能分析变更内容，生成更新日志
- 支持手动触发强制更新
- 多渠道通知更新内容
- 版本管理和历史记录查询

**使用方法：**
1. 下载技能压缩包并解压到 OpenClaw 技能目录
2. 运行 `scripts/install.sh` 安装依赖
3. 在 `config/config.yaml` 中配置通知渠道
4. 通过技能指令调用：
   - `/claudecode-tutorial check` 检查更新
   - `/claudecode-tutorial force-update` 强制更新
   - `/claudecode-tutorial version` 查看当前版本
   - `/claudecode-tutorial history` 查看更新历史

**目录结构：**
```
claudecode-tutorial-updater/
├── config/          # 配置文件目录
├── src/             # 核心源代码
├── scripts/         # 安装/卸载脚本
├── commands/        # 指令说明文档
├── README.md        # 技能详细说明
└── skill.json       # 技能元数据
```

## 🔧 配置说明
所有配置可在 `config/config.yaml` 中修改：

### 检测配置
```yaml
check:
  # 检查频率：hourly(每小时)/6hourly(每6小时)/daily(每天)
  frequency: "daily"
  # 执行时间（cron表达式，默认每天凌晨2点）
  schedule: "0 2 * * *"
  
  # 监测渠道（默认全部开启）
  channels:
    official_docs: "https://docs.anthropic.com/claude/docs"       # 官方文档
    github_repo: "https://github.com/anthropics/claude-code"      # GitHub仓库
    release_notes: "https://www.anthropic.com/release-notes"      # 发布说明
    plugin_market: "https://plugins.claude.ai"                    # 插件市场
    discord_announcements: "Discord官方公告频道"                   # Discord公告
```

### 通知配置
```yaml
notify:
  # 通知方式：支持飞书(feishu)/邮件(email)
  channels: ["feishu"]
  # 飞书webhook地址（需自行配置）
  feishu_webhook: ""
  # 告警阈值：critical(严重)/major(重要)/minor(次要)
  alert_threshold: "major"
```

### 更新配置
```yaml
update:
  # 本地教程仓库路径
  repo_path: "/workspace/projects/claudecode-book"
  # 自动提交变更到Git
  auto_commit: true
  # 自动推送到远程仓库（默认关闭）
  auto_push: false
  # 更新前自动备份
  auto_backup: true
  # 备份文件存储路径
  backup_path: "/workspace/backup/claudecode-book"
```

### 优先级配置
```yaml
priority:
  # 不同变更类型的响应时间（小时）
  critical: 24   # 功能变更、安全更新
  major: 72      # 教程新增、API更新
  minor: 168     # 文档优化、错别字修正
```
