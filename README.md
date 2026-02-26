# Seedance 2.0 视频生成助手
# 跨平台命令行工具

## 功能
- 通过交互式问答收集视频创作需求
- AI 辅助扩展建议（当用户难以回答时）
- 直接提交到 Seedance 2.0 API 生成视频

## 安装
```bash
pip install -r requirements.txt
```

## 配置
首次运行后，会在用户目录创建 `~/.seedance_helper/config.yaml` 配置文件，请根据您的 API 信息进行配置。

## 使用
```bash
python main.py
```

## 依赖
- Python 3.8+
- pyyaml
- requests
- openai (用于 AI 扩展功能)
