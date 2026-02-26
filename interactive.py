# -*- coding: utf-8 -*-
"""
增强版交互式问答 - 支持 AI 辅助
"""

import os
from typing import Optional, List
from questionnaire import Question, VideoRequirements, Scene
from ai_extension import AIExtension, demo_ai_suggestions


def enhanced_questionnaire(ai: Optional[AIExtension] = None) -> VideoRequirements:
    """增强版问卷系统，支持 AI 辅助"""

    # 基础信息收集
    requirements = VideoRequirements()

    print("\n" + "="*60)
    print("🎬 Seedance 2.0 视频生成助手")
    print("="*60)
    print("\n让我们开始创建你的视频！")
    print("\n💡 提示: 回答问题时，可以输入 'ai' 获取 AI 建议")
    print("="*60)

    # 第一部分：主题与故事
    print("\n📝 第一部分：主题与故事")
    print("-"*40)

    requirements.theme = ask_with_ai(
        "📝 视频主题/标题",
        "你希望制作一个关于什么主题的视频？例如：城市夜景、自然风光、产品展示等",
        ai
    )

    requirements.story = ask_with_ai(
        "📖 故事描述",
        "描述你想讲述的故事或展示的内容，越详细越好",
        ai
    )

    # 第二部分：整体风格
    print("\n🎨 第二部分：整体风格")
    print("-"*40)

    # 整体格调
    print("\n💡 提示: 不知道如何选择时，输入 'ai' 获取专业建议")
    requirements.overall_style = ask_with_options_and_ai(
        "🎨 整体格调",
        "你希望视频呈现什么样的风格？",
        [
            ("电影感", "电影级的画面质感和叙事风格"),
            ("纪录片风格", "真实、客观的记录形式"),
            ("时尚潮流", "现代、炫酷的视觉风格"),
            ("温馨治愈", "温暖、柔和的氛围"),
            ("赛博朋克", "未来科技感"),
            ("复古怀旧", "怀旧、复古的色调"),
            ("极简主义", "简洁、干练的画面"),
            ("自然清新", "清爽、自然的视觉效果")
        ],
        ai,
        requirements.theme
    )

    requirements.overall_lighting = ask_with_options_and_ai(
        "💡 整体光照",
        "你希望视频整体的光线效果是怎样的？",
        [
            ("自然光", "模拟日光、月光等自然光源"),
            ("柔光", "柔和、均匀的布光"),
            ("硬光", "强烈对比的明暗效果"),
            ("背光", "逆光剪影效果"),
            ("霓虹灯", "赛博朋克风格的灯光"),
            ("暖色调光", "温馨的暖黄色调"),
            ("冷色调光", "清凉的冷蓝色调"),
            ("戏剧性光影", "强烈的明暗对比")
        ],
        ai,
        requirements.theme
    )

    requirements.color_tone = ask_with_options_and_ai(
        "🎭 色调",
        "你希望视频整体呈现什么颜色倾向？",
        [
            ("中性灰", "真实自然的色彩"),
            ("暖色调", "橙黄色系的温暖感"),
            ("冷色调", "蓝绿色系的冷峻感"),
            ("高饱和度", "鲜艳夺目的色彩"),
            ("低饱和度", "柔和淡雅的色调"),
            ("黑白/单色", "经典的黑白风格"),
            ("电影调色", "专业的电影色彩分级"),
            ("复古色调", "怀旧的色彩风格")
        ],
        ai,
        requirements.theme
    )

    # 第三部分：镜头设置
    print("\n📷 第三部分：镜头设置")
    print("-"*40)

    requirements.lens_selection = ask_with_options_and_ai(
        "📷 镜头选型",
        "你希望使用什么类型的镜头效果？",
        [
            ("广角镜头", "宽广的视野，适合风景"),
            ("标准镜头", "接近人眼视角，自然真实"),
            ("长焦镜头", "压缩空间，突出主体"),
            ("微距镜头", "拍摄微小细节"),
            ("鱼眼镜头", "夸张的透视效果"),
            ("推拉镜头", "动态的镜头运动"),
            ("斯坦尼康", "平滑的稳定运动"),
            ("航拍镜头", "俯瞰视角")
        ],
        ai,
        requirements.theme
    )

    requirements.aspect_ratio = ask_with_options_and_ai(
        "📐 屏幕比例",
        "视频的宽高比是多少？",
        [
            ("16:9", "标准横屏（最常用）"),
            ("9:16", "竖屏（短视频平台）"),
            ("1:1", "方形（社交媒体）"),
            ("21:9", "电影宽屏"),
            ("4:3", "传统电视比例")
        ],
        ai,
        requirements.theme,
        default="16:9"
    )

    # 第四部分：时间节奏
    print("\n⏱️ 第四部分：时间节奏")
    print("-"*40)

    requirements.total_duration = ask_numeric(
        "⏱️ 视频总时长（秒）",
        "你希望视频总时长是多少秒？",
        default=30
    )

    requirements.rhythm = ask_with_options_and_ai(
        "🎵 节奏",
        "你希望视频的整体节奏是怎样的？",
        [
            ("快节奏", "快速切换，充满活力"),
            ("中节奏", "平衡的叙事节奏"),
            ("慢节奏", "舒缓、从容的氛围"),
            ("由慢到快", "渐进式的节奏变化"),
            ("由快到慢", "渐入式的节奏变化"),
            ("快慢交替", "富有变化的节奏")
        ],
        ai,
        requirements.theme
    )

    # 第五部分：分镜头
    print("\n📹 第五部分：分镜头设置")
    print("-"*40)

    num_scenes = ask_numeric(
        "📹 分镜头数量",
        f"根据总时长 {requirements.total_duration} 秒，建议分为 {max(1, int(requirements.total_duration/5))} 个分镜头\n请输入分镜头数量 (1-9)",
        min_val=1,
        max_val=9,
        default=max(1, int(requirements.total_duration/5))
    )

    for i in range(num_scenes):
        print(f"\n{'='*40}")
        print(f"📹 分镜头 {i+1}/{num_scenes}")
        print("="*40)

        scene = Scene(
            index=i+1,
            duration=ask_numeric(
                f"  时长",
                f"  第 {i+1} 个分镜头持续多少秒？",
                default=requirements.total_duration / num_scenes
            ),
            camera_angle="",
            description="",
            transition_to_next="直接切换"
        )

        scene.camera_angle = ask_with_options_and_ai(
            f"  镜头机位",
            f"  使用什么角度的镜头？",
            [
                ("正面", "正面面对主体"),
                ("侧面", "90度侧拍"),
                ("斜侧", "45度角拍摄"),
                ("低角度", "仰视视角"),
                ("高角度", "俯视视角"),
                ("俯冲", "从高处冲向主体"),
                ("升格", "从低处升起的视角"),
                ("旋转", "环绕主体旋转")
            ],
            ai,
            requirements.theme
        )

        scene.description = ask_with_ai(
            f"  场景描述",
            f"  详细描述第 {i+1} 个分镜头要展示什么内容",
            ai,
            requirements.overall_style
        )

        if i < num_scenes - 1:
            scene.transition_to_next = ask_with_options_and_ai(
                f"  过渡效果",
                f"  这个镜头与下一个镜头之间如何过渡？",
                [
                    ("直接切换", "无过渡直接切换"),
                    ("淡入淡出", "渐变过渡"),
                    ("交叉溶解", "叠化效果"),
                    ("擦除", "方向性过渡"),
                    ("缩放过渡", "缩放效果连接"),
                    ("模糊过渡", "虚化过渡"),
                    ("黑场过渡", "通过黑场过渡"),
                    ("匹配剪辑", "基于相似性过渡")
                ],
                ai,
                requirements.theme
            )

        requirements.scenes.append(scene)

    # 第六部分：素材
    print("\n🖼️ 第六部分：参考素材（可选）")
    print("-"*40)

    print("\n参考图片路径 (每行一个路径，直接回车结束):")
    while True:
        img = input("  > ").strip()
        if not img:
            break
        requirements.images.append(img)

    print("\n参考视频路径 (每行一个路径，直接回车结束):")
    while True:
        vid = input("  > ").strip()
        if not vid:
            break
        requirements.videos.append(vid)

    print("\n背景音乐路径 (每行一个路径，直接回车结束):")
    while True:
        aud = input("  > ").strip()
        if not aud:
            break
        requirements.audios.append(aud)

    return requirements


def ask_with_ai(question: str, help_text: str,
                ai: Optional[AIExtension] = None,
                context: str = "") -> str:
    """带 AI 辅助的问题"""
    print(f"\n{question}")
    print(f"💡 {help_text}")
    print("💡 输入 'ai' 获取 AI 建议")
    print("> ", end="")

    answer = input().strip()

    # 如果用户输入 ai
    if answer.lower() == "ai":
        return get_ai_suggestion(question, help_text, ai, context)

    while not answer:
        print("⚠️ 请输入内容，或输入 'ai' 寻求 AI 帮助")
        print("> ", end="")
        answer = input().strip()
        if answer.lower() == "ai":
            return get_ai_suggestion(question, help_text, ai, context)

    return answer


def ask_with_options_and_ai(question: str, help_text: str,
                          options: List[tuple],
                          ai: Optional[AIExtension] = None,
                          context: str = "",
                          default: str = "") -> str:
    """带选项和 AI 辅助的问题"""
    print(f"\n{question}")
    print(f"💡 {help_text}")

    # 显示选项
    print("\n可选值:")
    for i, (key, desc) in enumerate(options, 1):
        print(f"  {i}. {key} - {desc}")

    print("💡 输入数字选择，或输入 'ai' 获取 AI 建议")
    if default:
        print(f"💡 直接回车使用默认值: {default}")
    print("> ", end="")

    answer = input().strip()

    # AI 建议
    if answer.lower() == "ai":
        return get_ai_suggestion_with_options(question, options, ai, context)

    # 数字选择
    if answer.isdigit():
        idx = int(answer) - 1
        if 0 <= idx < len(options):
            return options[idx][0]

    # 默认值
    if not answer and default:
        return default

    # 返回用户输入
    if answer:
        return answer

    # 重试
    print("⚠️ 请输入有效选项")
    return ask_with_options_and_ai(question, help_text, options, ai, context, default)


def get_ai_suggestion(question: str, help_text: str,
                     ai: Optional[AIExtension],
                     context: str) -> str:
    """获取 AI 建议"""
    if ai and ai.is_available():
        print("\n🤖 正在请求 AI 助手...")
        result = ai.generate_suggestions(context, question, "")
        if result and result.suggestions:
            print("\n📋 AI 建议:")
            for i, s in enumerate(result.suggestions, 1):
                print(f"  {i}. {s}")

            print("\n请选择或输入你的想法:")
            print("> ", end="")
            choice = input().strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(result.suggestions):
                    return result.suggestions[idx]
            return choice if choice else result.suggestions[0]

    # 使用内置建议
    return get_builtin_suggestion(question)


def get_ai_suggestion_with_options(question: str,
                                   options: List[tuple],
                                   ai: Optional[AIExtension],
                                   context: str) -> str:
    """获取带选项的 AI 建议"""
    if ai and ai.is_available():
        print("\n🤖 正在请求 AI 助手...")
        result = ai.generate_suggestions(context, question, "")
        if result and result.suggestions:
            print("\n📋 AI 推荐选项:")
            all_options = options.copy()
            for i, s in enumerate(result.suggestions):
                key = s.split(" - ")[0] if " - " in s else s
                desc = s.split(" - ")[1] if " - " in s else ""
                all_options.append((key, desc))

            for i, (key, desc) in enumerate(all_options, 1):
                print(f"  {i}. {key}" + (f" - {desc}" if desc else ""))

            print("\n请选择:")
            print("> ", end="")
            choice = input().strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(all_options):
                    return all_options[idx][0]

    # 使用内置建议
    return get_builtin_suggestion(question)


def get_builtin_suggestion(question: str) -> str:
    """获取内置建议"""
    suggestions = demo_ai_suggestions()

    key_map = {
        "整体格调": "overall_style",
        "整体光照": "overall_lighting",
        "色调": "color_tone",
        "镜头选型": "lens_selection",
        "节奏": "rhythm"
    }

    for keyword, key in key_map.items():
        if keyword in question:
            opts = suggestions.get(key, [])
            if opts:
                print("\n📋 推荐选项:")
                for i, s in enumerate(opts, 1):
                    print(f"  {i}. {s}")

                print("\n请选择:")
                print("> ", end="")
                choice = input().strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(opts):
                        return opts[idx].split(" - ")[0]

    print("\n⚠️ 请根据你的想法输入内容")
    print("> ", end="")
    return input().strip()


def ask_numeric(question: str, help_text: str,
               min_val: float = 1, max_val: float = 999,
               default: float = 0) -> float:
    """询问数值"""
    print(f"\n{question}")
    print(f"💡 {help_text}")
    if default:
        print(f"💡 直接回车使用默认值: {default}")
    print("> ", end="")

    answer = input().strip()

    if not answer:
        return default

    try:
        value = float(answer)
        if min_val <= value <= max_val:
            return value
        else:
            print(f"⚠️ 请输入 {min_val}-{max_val} 之间的数值")
            return ask_numeric(question, help_text, min_val, max_val, default)
    except ValueError:
        print("⚠️ 请输入有效数字")
        return ask_numeric(question, help_text, min_val, max_val, default)


if __name__ == "__main__":
    # 测试
    req = enhanced_questionnaire()
    from questionnaire import print_requirements
    print_requirements(req)
