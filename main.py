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
from exporter import export_to_seedance_json, export_simple_json, print_json_preview


def get_default_download_dir() -> str:
    """获取用户默认下载目录"""
    # 首先尝试常见的下载目录
    possible_dirs = []

    if sys.platform == "win32":
        possible_dirs.append(os.path.join(os.path.expanduser("~"), "Downloads"))
    elif sys.platform == "darwin":  # macOS
        possible_dirs.append(os.path.join(os.path.expanduser("~"), "Downloads"))
    else:  # Linux
        possible_dirs.append(os.path.join(os.path.expanduser("~"), "下载"))  # 中文
        possible_dirs.append(os.path.join(os.path.expanduser("~"), "Downloads"))  # 英文
        xdg_download = os.environ.get("XDG_DOWNLOAD_DIR")
        if xdg_download:
            possible_dirs.append(xdg_download)

    # 尝试查找存在的目录
    for d in possible_dirs:
        if os.path.exists(d) and os.path.isdir(d):
            return d

    # 如果都不存在，使用用户主目录
    return os.path.expanduser("~")


def preview_and_confirm_export(requirements: VideoRequirements) -> tuple:
    """
    预览JSON并确认是否需要修改
    返回: (是否继续, 是否导出, 导出路径)
    """
    # 生成 JSON 数据
    json_data = export_to_seedance_json(requirements)

    # 打印 JSON 预览
    print_json_preview(json_data)

    # 询问是否需要修改
    print("\n是否需要修改以上内容？")
    print("  1. 是，我要修改某一项")
    print("  2. 否，继续下一步")
    print("  0. 取消，退出程序")
    print("> ", end="")

    choice = input().strip()

    if choice == "0":
        return False, False, None
    elif choice == "1":
        # 让用户选择要修改的项目
        while True:
            print("\n请选择要修改的项目：")
            print("  1. 主题")
            print("  2. 故事描述")
            print("  3. 整体格调")
            print("  4. 光照")
            print("  5. 色调")
            print("  6. 镜头选型")
            print("  7. 屏幕比例")
            print("  8. 总时长")
            print("  9. 节奏")
            print("  10. 分镜头设置")
            print("  11. 参考素材")
            print("  0. 返回上一步")
            print("> ", end="")

            mod_choice = input().strip()

            if mod_choice == "0":
                break
            elif mod_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                print("\n⚠️ 当前版本暂不支持直接修改，请在重新运行问卷时输入正确的内容")
                print("是否重新运行问卷？(y/n)")
                print("> ", end="")
                if input().strip().lower() == "y":
                    return None, False, None  # None 表示需要重新运行
                break
            else:
                print("⚠️ 无效选择")

    # 继续流程，询问是否导出
    return True, None, None


def ask_export_json(requirements: VideoRequirements, theme: str) -> tuple:
    """
    询问用户是否导出JSON
    返回: (是否导出, 导出路径)
    """
    print("\n是否导出 Seedance 2.0 格式的 JSON 文件？")
    print("  1. 导出到默认目录（下载文件夹）")
    print("  2. 导出到自定义路径")
    print("  3. 不导出")
    print("> ", end="")

    choice = input().strip()

    if choice == "1":
        # 导出到默认目录
        default_dir = get_default_download_dir()
        default_filename = f"seedance_{theme or 'video'}.json"
        default_path = os.path.join(default_dir, default_filename)

        print(f"\n默认导出路径: {default_path}")
        print("直接回车使用默认路径，或输入新的文件名:")

        # 检查目录是否存在
        if not os.path.exists(default_dir):
            print(f"⚠️ 目录不存在，将创建: {default_dir}")
            os.makedirs(default_dir, exist_ok=True)

        filename = input(f"  > ({default_filename}): ").strip()
        export_path = os.path.join(default_dir, filename) if filename else default_path

        return True, export_path
    elif choice == "2":
        # 自定义路径
        print("\n请输入完整的文件路径:")
        print("  > ", end="")
        custom_path = input().strip()
        if custom_path:
            return True, custom_path
        else:
            print("⚠️ 未输入路径，取消导出")
            return False, None
    else:
        return False, None


def confirm_cancel(action: str = "提交"):
    """
    确认取消操作
    返回: 是否确认取消
    """
    print(f"\n⚠️ 确认取消 {action} 吗？")
    print("   取消后，你本次填写的内容将不会被保存！")
    print("   请确认是否取消？")
    print("  1. 确认取消")
    print("  2. 继续操作")
    print("> ", end="")

    choice = input().strip()
    return choice == "1"

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
        # 运行交互式问卷
        requirements = run_interactive_mode(config, args.skip_ai, args.interactive)

        # 预览并确认
        if args.dry_run:
            print("\n📝 模式: 预览模式（不提交）")
        else:
            print("\n🚀 模式: 提交到 Seedance API")

        # 预览 JSON 并确认（只有在非导出模式下才需要预览）
        if args.export:
            # 命令行指定了导出路径，直接导出
            export_to_seedance_json(requirements, args.export)
        else:
            # 交互式预览 JSON
            continue_flow, need_rerun, _ = preview_and_confirm_export(requirements)

            # 处理需要重新运行的情况
            if need_rerun is None:
                # 用户选择重新运行问卷
                print("\n请重新运行程序")
                return

            if not continue_flow:
                # 用户取消
                if confirm_cancel("预览"):
                    print("\n已取消，成果未保存")
                    return
                else:
                    # 用户取消取消，继续流程
                    continue_flow = True

            if continue_flow:
                # 询问是否导出 JSON
                should_export, export_path = ask_export_json(requirements, requirements.theme)

                if should_export and export_path:
                    try:
                        export_to_seedance_json(requirements, export_path)
                    except Exception as e:
                        print(f"⚠️ 导出失败: {e}")
                        print("是否重试？(y/n)")
                        if input("  > ").strip().lower() == "y":
                            try:
                                new_path = input("请输入新的文件路径: ").strip()
                                if new_path:
                                    export_to_seedance_json(requirements, new_path)
                            except Exception as e2:
                                print(f"⚠️ 导出失败: {e2}")

                # 检查 API 密钥并提交
                api_key = config.get("api", {}).get("api_key", "")
                has_api_key = api_key and api_key != "your_api_key_here"

                if not has_api_key:
                    print("\n⚠️ 未配置 API 密钥，无法提交到 Seedance API")
                    print("你可以:")
                    print("  1. 配置 API 密钥后重新运行来提交生成")
                    print("  2. 使用已导出的 JSON 文件在其他平台生成")
                else:
                    # 确认提交
                    print("\n" + "="*60)
                    print("确认提交到 Seedance API 生成视频？")
                    print("(输入 'y' 确认，输入 'n' 取消)")
                    print("> ", end="")

                    if input().strip().lower() == "y":
                        # 创建 API 客户端
                        client = SeedanceClient(
                            base_url=config.get("api", {}).get("base_url", "https://api.seedance2-ai.io"),
                            api_key=api_key
                        )
                        # 提交请求
                        submit_video_request(client, requirements)
                    else:
                        # 用户取消提交，需要确认
                        if confirm_cancel("提交"):
                            print("\n已取消提交")
                            print("你可以通过 --dry-run 模式重新预览")
                        else:
                            # 用户取消取消，继续尝试提交
                            print("\n请再次确认是否提交...")
                            print("> ", end="")
                            if input().strip().lower() == "y":
                                client = SeedanceClient(
                                    base_url=config.get("api", {}).get("base_url", "https://api.seedance2-ai.io"),
                                    api_key=api_key
                                )
                                submit_video_request(client, requirements)

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
