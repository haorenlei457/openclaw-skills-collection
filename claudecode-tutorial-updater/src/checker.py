#!/usr/bin/env python3
"""
Claude Code官方更新检查器
"""

import os
import json
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import yaml

class UpdateChecker:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.state_file = os.path.join(os.path.dirname(__file__), '../state/last_check.json')
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
        self.last_state = self._load_last_state()
    
    def _load_last_state(self):
        """加载上次检查状态"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """保存当前检查状态"""
        with open(self.state_file, 'w') as f:
            json.dump(self.last_state, f, indent=2, ensure_ascii=False)
    
    def _get_content_hash(self, content):
        """计算内容哈希值"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def check_official_docs(self):
        """检查官方文档更新"""
        channel = self.config['check']['channels']['official_docs']
        if not channel['enabled']:
            return []
        
        changes = []
        try:
            response = requests.get(channel['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text(strip=True)
            current_hash = self._get_content_hash(content)
            
            last_hash = self.last_state.get('official_docs', {}).get('hash')
            if last_hash and current_hash != last_hash:
                changes.append({
                    'type': 'doc_update',
                    'source': 'official_docs',
                    'url': channel['url'],
                    'timestamp': datetime.now().isoformat(),
                    'title': '官方文档更新'
                })
            
            self.last_state['official_docs'] = {
                'hash': current_hash,
                'last_check': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"检查官方文档失败: {e}")
        
        return changes
    
    def check_github_repo(self):
        """检查GitHub仓库更新"""
        channel = self.config['check']['channels']['github_repo']
        if not channel['enabled']:
            return []
        
        changes = []
        try:
            api_url = "https://api.github.com/repos/anthropics/claude-code/commits"
            params = {'per_page': 5}
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            
            commits = response.json()
            last_commit_sha = self.last_state.get('github_repo', {}).get('last_sha')
            
            if last_commit_sha:
                new_commits = [c for c in commits if c['sha'] != last_commit_sha]
                if new_commits:
                    for commit in new_commits[:3]:  # 只取最近3个提交
                        changes.append({
                            'type': 'code_update',
                            'source': 'github_repo',
                            'url': commit['html_url'],
                            'timestamp': commit['commit']['author']['date'],
                            'title': commit['commit']['message'].split('\n')[0],
                            'author': commit['commit']['author']['name']
                        })
            
            if commits:
                self.last_state['github_repo'] = {
                    'last_sha': commits[0]['sha'],
                    'last_check': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"检查GitHub仓库失败: {e}")
        
        return changes
    
    def check_release_notes(self):
        """检查发布公告更新"""
        channel = self.config['check']['channels']['release_notes']
        if not channel['enabled']:
            return []
        
        changes = []
        try:
            response = requests.get(channel['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            
            last_article_title = self.last_state.get('release_notes', {}).get('last_title')
            
            if articles:
                latest_article = articles[0]
                title = latest_article.find('h2').get_text(strip=True) if latest_article.find('h2') else latest_article.get_text(strip=True)[:50]
                
                if last_article_title and title != last_article_title:
                    changes.append({
                        'type': 'release',
                        'source': 'release_notes',
                        'url': channel['url'],
                        'timestamp': datetime.now().isoformat(),
                        'title': f"新版本发布: {title}"
                    })
                
                self.last_state['release_notes'] = {
                    'last_title': title,
                    'last_check': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"检查发布公告失败: {e}")
        
        return changes
    
    def check_plugin_market(self):
        """检查插件市场更新"""
        channel = self.config['check']['channels']['plugin_market']
        if not channel['enabled']:
            return []
        
        changes = []
        try:
            # 插件市场API
            api_url = "https://plugins.claude.ai/api/plugins"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            plugins = response.json()
            last_plugin_count = self.last_state.get('plugin_market', {}).get('count', 0)
            
            if len(plugins) != last_plugin_count:
                if len(plugins) > last_plugin_count:
                    new_plugins = len(plugins) - last_plugin_count
                    changes.append({
                        'type': 'new_plugin',
                        'source': 'plugin_market',
                        'url': channel['url'],
                        'timestamp': datetime.now().isoformat(),
                        'title': f"新增{new_plugins}个官方插件"
                    })
                
                self.last_state['plugin_market'] = {
                    'count': len(plugins),
                    'last_check': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"检查插件市场失败: {e}")
        
        return changes
    
    def check_all(self):
        """检查所有渠道"""
        all_changes = []
        
        all_changes.extend(self.check_official_docs())
        all_changes.extend(self.check_github_repo())
        all_changes.extend(self.check_release_notes())
        all_changes.extend(self.check_plugin_market())
        
        self._save_state()
        return all_changes

if __name__ == "__main__":
    checker = UpdateChecker()
    changes = checker.check_all()
    
    if changes:
        print(f"发现 {len(changes)} 个变更:")
        for change in changes:
            print(f"- [{change['type']}] {change['title']} ({change['source']})")
    else:
        print("没有发现新的变更")
