#!/usr/bin/env python3
"""
内容更新器 - 自动更新教程内容
"""

import os
import json
import yaml
import subprocess
from datetime import datetime
import shutil

class TutorialUpdater:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.repo_path = self.config['update']['repo_path']
        self.backup_path = self.config['update']['backup_path']
        
        os.makedirs(self.repo_path, exist_ok=True)
        os.makedirs(self.backup_path, exist_ok=True)
    
    def _run_git_command(self, command, cwd=None):
        """执行Git命令"""
        if cwd is None:
            cwd = self.repo_path
        
        try:
            result = subprocess.run(
                ['git'] + command.split(),
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def backup_tutorial(self):
        """备份当前教程"""
        if not self.config['update']['auto_backup']:
            return True, "备份已禁用"
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(self.backup_path, f"backup_{timestamp}")
        
        try:
            shutil.copytree(self.repo_path, backup_dir)
            return True, f"备份完成: {backup_dir}"
        except Exception as e:
            return False, f"备份失败: {e}"
    
    def pull_latest(self):
        """拉取最新代码"""
        success, output = self._run_git_command("pull origin main")
        return success, output
    
    def commit_changes(self, message):
        """提交变更"""
        if not self.config['update']['auto_commit']:
            return True, "自动提交已禁用"
        
        self._run_git_command("add .")
        success, output = self._run_git_command(f'commit -m "{message}"')
        return success, output
    
    def push_changes(self):
        """推送变更到远程"""
        if not self.config['update']['auto_push']:
            return True, "自动推送已禁用"
        
        success, output = self._run_git_command("push origin main")
        return success, output
    
    def update_chapter(self, chapter_file, new_content):
        """更新指定章节内容"""
        file_path = os.path.join(self.repo_path, chapter_file)
        
        if not os.path.exists(file_path):
            return False, f"文件不存在: {chapter_file}"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"更新成功: {chapter_file}"
        except Exception as e:
            return False, f"更新失败: {e}"
    
    def append_to_chapter(self, chapter_file, content):
        """追加内容到章节"""
        file_path = os.path.join(self.repo_path, chapter_file)
        
        if not os.path.exists(file_path):
            return False, f"文件不存在: {chapter_file}"
        
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n' + content)
            return True, f"追加内容成功: {chapter_file}"
        except Exception as e:
            return False, f"追加内容失败: {e}"
    
    def add_new_chapter(self, chapter_number, title, content):
        """新增章节"""
        chapter_file = f"{chapter_number:02d}-{title.lower().replace(' ', '-')}.md"
        file_path = os.path.join(self.repo_path, chapter_file)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 更新README目录
            self._update_readme_toc(chapter_number, title, chapter_file)
            
            return True, f"新增章节成功: {chapter_file}"
        except Exception as e:
            return False, f"新增章节失败: {e}"
    
    def _update_readme_toc(self, chapter_number, title, chapter_file):
        """更新README的目录"""
        readme_path = os.path.join(self.repo_path, 'README.md')
        
        if not os.path.exists(readme_path):
            return
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 找到核心教程表格
            toc_start = content.find("## 📖 核心教程")
            toc_end = content.find("---", toc_start)
            
            if toc_start == -1 or toc_end == -1:
                return
            
            toc_content = content[toc_start:toc_end]
            
            # 找到最后一个章节行
            lines = toc_content.split('\n')
            last_chapter_line = None
            for line in lines:
                if line.startswith('| ') and line[2].isdigit():
                    last_chapter_line = line
            
            if last_chapter_line:
                # 插入新章节行
                new_line = f"| {chapter_number} | [{title}](./{chapter_file}) | ⭐⭐⭐ | 45min |"
                new_toc = toc_content.replace(last_chapter_line, f"{last_chapter_line}\n{new_line}")
                content = content.replace(toc_content, new_toc)
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        except Exception as e:
            print(f"更新README目录失败: {e}")
    
    def update_code_examples(self, old_pattern, new_content):
        """批量更新代码示例"""
        updated_files = []
        errors = []
        
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if old_pattern in content:
                            new_content_file = content.replace(old_pattern, new_content)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content_file)
                            updated_files.append(file_path)
                    
                    except Exception as e:
                        errors.append(f"{file_path}: {e}")
        
        return updated_files, errors
    
    def run_update(self, change, content_updates):
        """执行更新流程"""
        results = []
        
        # 1. 备份
        success, msg = self.backup_tutorial()
        results.append(msg)
        if not success:
            return False, results
        
        # 2. 拉取最新代码
        success, msg = self.pull_latest()
        results.append(msg)
        if not success:
            return False, results
        
        # 3. 执行内容更新
        for update in content_updates:
            if update['type'] == 'update_chapter':
                success, msg = self.update_chapter(update['file'], update['content'])
            elif update['type'] == 'append_chapter':
                success, msg = self.append_to_chapter(update['file'], update['content'])
            elif update['type'] == 'new_chapter':
                success, msg = self.add_new_chapter(
                    update['number'],
                    update['title'],
                    update['content']
                )
            elif update['type'] == 'update_code':
                updated, errors = self.update_code_examples(update['old'], update['new'])
                success = len(errors) == 0
                msg = f"更新了 {len(updated)} 个文件"
                if errors:
                    msg += f", 错误: {len(errors)}个"
            else:
                success = False
                msg = f"未知更新类型: {update['type']}"
            
            results.append(msg)
            if not success:
                return False, results
        
        # 4. 提交变更
        commit_message = f"docs: 同步官方更新 - {change['title']}"
        success, msg = self.commit_changes(commit_message)
        results.append(msg)
        if not success:
            return False, results
        
        # 5. 推送变更
        success, msg = self.push_changes()
        results.append(msg)
        
        return True, results

if __name__ == "__main__":
    updater = TutorialUpdater()
    
    # 测试备份
    success, msg = updater.backup_tutorial()
    print(msg)
