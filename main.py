#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 视频生成助手 - 主程序入口
跨平台命令行工具
"""

import sys
import os
import argparse

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块
from config import ConfigManager, init_config
from questionnaire import VideoRequirements, print_requirements
from ai_extension import AIExtension, demo_ai_suggestions
from api_client import SeedanceClient, submit_video_request

# 尝试导入增强版问卷，如果失败则使用基础版
try:
    from interactive import enhanced_questionnaire
    USE_ENHANCED = True
except ImportError:
    from questionnaire import run_questionnaire
    USE_ENHANCED = False


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🎬  Seedance 2.0 视频生成助手                        ║
║                                                           ║
║     跨平台命令行工具 - 智能视频创作                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """检查依赖是否安装"""
    missing = []

    try:
        import yaml
    except ImportError:
        missing.append("pyyaml")

    try:
        import requests
    except ImportError:
        missing.append("requests")

    if missing:
        print("⚠️ 缺少依赖包，请安装:")
        print(f"   pip install {' '.join(missing)}")
        print()
        return False

    return True


def setup_argparse() -> argparse.ArgumentParser:
    """设置命令行参数"""
    parser = argparse.ArgumentParser(
        description="Seedance 2.0 视频生成助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                 # 启动交互式问答
  python main.py --skip-ai       # 跳过 AI 扩展
  python main.py --dry-run       # 仅预览不提交
  python main.py --config path   # 指定配置文件
        """
    )

    parser.add_argument(
        "--config", "-c",
        help="配置文件路径",
        default=None
    )

    parser.add_argument(
        "--skip-ai",
        action="store_true",
        help="跳过 AI 扩展功能"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅预览收集的信息，不提交到 API"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="使用交互式 AI 辅助"
    )

    parser.add_argument(
        "--export",
        "-e",
        help="导出需求到 JSON 文件",
        default=None
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser


def run_interactive_mode(config: dict, skip_ai: bool = False,
                         interactive_ai: bool = False) -> VideoRequirements:
    """运行交互式问答模式"""

    # 初始化 AI 扩展
    ai = None
    if not skip_ai and config.get("ai", {}).get("enabled", False):
        ai_key = config.get("ai", {}).get("openai_api_key", "")
        if ai_key and ai_key != "your_openai_api_key_here":
            ai = AIExtension(
                api_key=ai_key,
                model=config.get("ai", {}).get("model", "gpt-4"),
                base_url=config.get("ai", {}).get("base_url", "https://api.openai.com/v1")
            )
            if ai.is_available():
                print("✅ AI 扩展功能已启用")
            else:
                print("⚠️ AI 扩展功能不可用，将使用内置建议")
        else:
            print("⚠️ 未配置 OpenAI API 密钥，AI 扩展功能不可用")
            print("   将使用内置建议")

    # 运行问卷
    if USE_ENHANCED:
        requirements = enhanced_questionnaire(ai)
    else:
        from questionnaire import run_questionnaire
        requirements = run_questionnaire()

    # 打印摘要
    print_requirements(requirements)

    return requirements


def main():
    """主函数"""
    # 解析命令行参数
    parser = setup_argparse()
    args = parser.parse_args()

    # 打印横幅
    print_banner()

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 加载配置
    config_manager = ConfigManager(args.config)
    config = config_manager.load()

    # 检查 API 配置 (dry-run 模式下跳过)
    api_key = config.get("api", {}).get("api_key", "")
    if not args.dry_run and (not api_key or api_key == "your_api_key_here"):
        print("\n⚠️ 请先配置 API 密钥！")
        print(f"   配置文件: {config_manager.config_path}")
        print("\n编辑配置文件，将 'api_key' 改为你的实际密钥")
        print()

        # 创建配置文件供用户修改
        init_config()

        # 询问是否继续
        print("是否继续？(输入 'y' 继续，其他退出)")
        print("> ", end="")
        try:
            if input().strip().lower() != "y":
                sys.exit(0)
        except EOFError:
            print("\n⚠️ 非交互模式退出")
            sys.exit(0)

    # 根据参数运行不同模式
    try:
        if args.dry_run:
            print("\n📝 模式: 预览模式（不提交）")
            requirements = run_interactive_mode(config, args.skip_ai, args.interactive)

            # 导出到文件
            if args.export:
                import json
                with open(args.export, "w", encoding="utf-8") as f:
                    json.dump(requirements.to_dict(), f, ensure_ascii=False, indent=2)
                print(f"\n✅ 已导出到: {args.export}")

        else:
            print("\n🚀 模式: 提交到 Seedance API")
            requirements = run_interactive_mode(config, args.skip_ai, args.interactive)

            # 导出到文件
            if args.export:
                import json
                with open(args.export, "w", encoding="utf-8") as f:
                    json.dump(requirements.to_dict(), f, ensure_ascii=False, indent=2)
                print(f"\n✅ 已导出到: {args.export}")

            # 确认提交
            print("\n" + "="*60)
            print("确认提交到 Seedance API 生成视频？")
            print("(输入 'y' 确认，其他取消)")
            print("> ", end="")

            if input().strip().lower() == "y":
                # 创建 API 客户端
                client = SeedanceClient(
                    base_url=config.get("api", {}).get("base_url", "https://api.seedance2-ai.io"),
                    api_key=config.get("api", {}).get("api_key", "")
                )

                # 提交请求
                submit_video_request(client, requirements)
            else:
                print("\n已取消提交")
                print("你可以通过 --dry-run 模式重新预览")

    except KeyboardInterrupt:
        print("\n\n⚠️ 已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n👋 感谢使用 Seedance 2.0 视频生成助手！")


if __name__ == "__main__":
    main()
