# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


DEFAULT_CONFIG_DIR = "~/.seedance_helper"
DEFAULT_CONFIG_FILE = "~/.seedance_helper/config.yaml"
CONFIG_TEMPLATE = "config_template.yaml"


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: Optional[str] = None):
        expanded_path = os.path.expanduser(config_path or DEFAULT_CONFIG_FILE)
        self.config_path = expanded_path
        self.config_dir = os.path.dirname(expanded_path)
        self.config: Dict[str, Any] = {}
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        os.makedirs(self.config_dir, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """加载配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = self._get_default_config()
            self.save()
            print(f"✅ 已创建默认配置文件: {self.config_path}")
            print("请编辑配置文件，填入你的 API 密钥")

        return self.config

    def save(self):
        """保存配置"""
        self._ensure_config_dir()
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any):
        """设置配置项"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "api": {
                "base_url": "https://api.seedance2-ai.io",
                "api_key": "your_api_key_here",
                "endpoints": {
                    "generate": "/v1/video/generate",
                    "query": "/v1/video/query"
                }
            },
            "ai": {
                "enabled": True,
                "openai_api_key": "your_openai_api_key_here",
                "model": "gpt-4",
                "base_url": "https://api.openai.com/v1"
            },
            "defaults": {
                "aspect_ratio": "16:9",
                "fps": 24,
                "quality": "high"
            }
        }

    def create_template(self):
        """创建配置模板文件"""
        template_path = os.path.join(self.config_dir, "config_template.yaml")

        if not os.path.exists(template_path):
            default_config = self._get_default_config()
            with open(template_path, "w", encoding="utf-8") as f:
                yaml.dump(default_config, f, allow_unicode=True, default_flow_style=False)

        return template_path


def get_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """获取配置"""
    manager = ConfigManager(config_path)
    return manager.load()


def save_config(config: Dict[str, Any], config_path: Optional[str] = None):
    """保存配置"""
    manager = ConfigManager(config_path)
    manager.config = config
    manager.save()


def init_config() -> ConfigManager:
    """初始化配置"""
    manager = ConfigManager()

    if not os.path.exists(manager.config_path):
        manager.config = manager._get_default_config()
        manager.save()
        print(f"\n✅ 已创建配置文件: {manager.config_path}")
        print("="*60)
        print("⚠️ 请编辑配置文件，填入以下信息:")
        print("   - Seedance API 密钥")
        print("   - (可选) OpenAI API 密钥用于 AI 扩展功能")
        print("="*60)

    return manager


if __name__ == "__main__":
    manager = init_config()
    print("\n当前配置:")
    print(yaml.dump(manager.config, allow_unicode=True, default_flow_style=False))
