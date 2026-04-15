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
