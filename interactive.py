# -*- coding: utf-8 -*-
"""
增强版交互式问答 - 支持 AI 辅助、回退功能、输入校验
包含：经典电影参考、场景模板、情绪板、镜头组合等功能
"""

import os
from typing import Optional, List, Dict, Any, Callable
from questionnaire import Question, VideoRequirements, Scene
from ai_extension import AIExtension, demo_ai_suggestions
from film_data import (
    get_film_references, get_scene_templates, get_mood_board,
    get_camera_guide, get_shot_combinations, FILM_REFERENCE,
    SCENE_TEMPLATES, MOOD_BOARD, CAMERA_GUIDE, SHOT_COMBINATIONS
)


class QuestionnaireState:
    """问卷状态管理"""

    def __init__(self):
        self.step_history: List[Dict[str, Any]] = []
        self.current_section = ""
        self.answers: Dict[str, Any] = {}

    def save_step(self, section: str, question: str, answer: Any):
        """保存步骤"""
        self.step_history.append({
            "section": section,
            "question": question,
            "answer": answer
        })
        self.current_section = section

    def can_go_back(self) -> bool:
        """是否可以回退"""
        return len(self.step_history) > 1

    def go_back(self) -> Optional[Dict[str, Any]]:
        """回退到上一步"""
        if self.can_go_back():
            self.step_history.pop()
            if self.step_history:
                return self.step_history[-1]
        return None


def enhanced_questionnaire(ai: Optional[AIExtension] = None) -> VideoRequirements:
    """增强版问卷系统，支持 AI 辅助、回退功能、输入校验"""

    # 基础信息收集
    requirements = VideoRequirements()
    state = QuestionnaireState()

    print("\n" + "="*60)
    print("🎬 Seedance 2.0 视频生成助手")
    print("="*60)
    print("\n让我们开始创建你的视频！")
    print("\n💡 提示: 回答问题时，可以输入 'ai' 获取 AI 建议")
    print("💡 输入 'b' 返回上一题")
    print("="*60)

    # ========== 0. 致敬大师环节 ==========
    print("\n🎬 第零部分：致敬大师（可选）")
    print("-"*40)
    state.current_section = "致敬大师"

    # 询问用户是否有喜欢的电影/镜头风格
    print("\n💡 你有没有特别喜欢的电影或镜头风格？")
    print("   看过经典电影吗？有没有哪个镜头让你印象深刻？")
    print("   输入你喜欢的电影名、镜头风格，或直接回车跳过")

    # 显示经典电影参考
    print("\n📚 经典电影镜头参考（按回车查看更多）:")
    film_refs = get_film_references()
    for i, film in enumerate(film_refs[:5], 1):
        print(f"  {i}. {film['name']} - {film['description']}")
        print(f"     导演: {film['director']} | 镜头: {film['camera_angle']}")

    print("  6. 查看更多电影...")
    print("  0. 跳过这一步")

    choice = input("\n> ").strip()

    selected_film = None
    if choice == "6":
        print("\n📚 更多经典电影参考:")
        for i, film in enumerate(film_refs, 1):
            print(f"  {i}. {film['name']} - {film['reference']}")
            print(f"     导演: {film['director']} | 适合场景: {film['tips']}")
        film_choice = input("\n选择你喜欢的电影编号: ").strip()
        if film_choice.isdigit() and 1 <= int(film_choice) <= len(film_refs):
            selected_film = film_refs[int(film_choice) - 1]
            print(f"\n✅ 已选择: {selected_film['name']}")
            print(f"   参考镜头: {selected_film['reference']}")
            print(f"   使用建议: {selected_film['tips']}")
    elif choice.isdigit() and 1 <= int(choice) <= 5:
        selected_film = film_refs[int(choice) - 1]
        print(f"\n✅ 已选择: {selected_film['name']}")

    # 第一部分：主题与故事
    print("\n📝 第一部分：主题与故事")
    print("-"*40)
    state.current_section = "主题与故事"

    requirements.theme = ask_with_ai(
        "📝 视频主题/标题",
        "你希望制作一个关于什么主题的视频？例如：城市夜景、自然风光、产品展示等",
        ai,
        state=state
    )

    requirements.story = ask_with_ai(
        "📖 故事描述",
        "描述你想讲述的故事或展示的内容，越详细越好",
        ai,
        state=state
    )

    # ========== 1.5 情绪板环节 ==========
    print("\n🎭 第一点五部分：情绪氛围")
    print("-"*40)
    state.current_section = "情绪氛围"

    print("\n💡 视频想要传达什么样的情感？")
    print("   选择一种情绪氛围，让我们帮你匹配最佳风格")

    mood_list = list(MOOD_BOARD.keys())
    print("\n可选情绪:")
    for i, mood in enumerate(mood_list, 1):
        info = MOOD_BOARD[mood]
        print(f"  {i}. {mood} - {info['description']}")

    print(f"  {len(mood_list)+1}. 我有自己的想法（手动设置）")
    print("  0. 跳过，使用默认设置")

    mood_choice = input("\n> ").strip()

    if mood_choice == "0":
        pass  # 跳过
    elif mood_choice.isdigit() and 1 <= int(mood_choice) <= len(mood_list):
        selected_mood = MOOD_BOARD[mood_list[int(mood_choice) - 1]]
        print(f"\n✅ 已选择情绪: {mood_list[int(mood_choice) - 1]}")
        print(f"   建议风格: {selected_mood['style']}")
        print(f"   建议光照: {selected_mood['lighting']}")
        print(f"   建议色调: {selected_mood['color_tone']}")
        # 自动填充建议值
        requirements.overall_style = selected_mood['style']
        requirements.overall_lighting = selected_mood['lighting']
        requirements.color_tone = selected_mood['color_tone']
        requirements.rhythm = selected_mood['rhythm']

    # 第二部分：整体风格（支持多选）
    print("\n🎨 第二部分：整体风格")
    print("-"*40)
    state.current_section = "整体风格"

    # 整体格调 - 支持多选
    print("\n💡 提示: 不知道如何选择时，输入 'ai' 获取专业建议")
    print("💡 支持多选，用逗号分隔（如：1,3,5）或输入范围（如：1-3）")
    requirements.overall_style = ask_with_multiple_options(
        "🎨 整体格调",
        "你希望视频呈现什么样的风格？（可多选）",
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
        requirements.theme,
        state=state
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
        requirements.theme,
        state=state
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
        requirements.theme,
        state=state
    )

    # 第三部分：镜头设置
    print("\n📷 第三部分：镜头设置")
    print("-"*40)
    state.current_section = "镜头设置"

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
        requirements.theme,
        state=state
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
        state=state,
        default="16:9"
    )

    # 第四部分：时间节奏
    print("\n⏱️ 第四部分：时间节奏")
    print("-"*40)
    state.current_section = "时间节奏"

    requirements.total_duration = ask_numeric(
        "⏱️ 视频总时长（秒）",
        "你希望视频总时长是多少秒？",
        default=15,
        min_val=1,
        max_val=300,
        state=state
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
        requirements.theme,
        state=state
    )

    # 第五部分：分镜头
    print("\n📹 第五部分：分镜头设置")
    print("-"*40)
    state.current_section = "分镜头设置"

    # 场景模板选择
    print("\n💡 你可以选择一个场景模板快速上手，或自己手动设置")
    print("   场景模板是专业摄影师常用的拍摄套路")

    scene_templates = get_scene_templates()
    template_list = list(scene_templates.keys())
    print("\n📖 可选场景模板:")
    for i, t in enumerate(template_list, 1):
        info = scene_templates[t]
        print(f"  {i}. {t} - {info['description']}")
    print(f"  {len(template_list)+1}. 我自己设置（不用模板）")
    print("  0. 跳过，稍后手动设置")

    template_choice = input("\n> ").strip()

    use_template = False
    selected_template = None

    if template_choice.isdigit():
        choice_num = int(template_choice)
        if 1 <= choice_num <= len(template_list):
            selected_template = scene_templates[template_list[choice_num - 1]]
            use_template = True
            print(f"\n✅ 已选择模板: {template_list[choice_num - 1]}")
            print(f"   包含 {len(selected_template['scenes'])} 个分镜头")
            print("   你可以在后面的设置中修改")

    num_scenes = ask_numeric(
        "📹 分镜头数量",
        f"根据总时长 {requirements.total_duration} 秒，建议分为 {max(1, int(requirements.total_duration/5))} 个分镜头\n请输入分镜头数量 (1-9)",
        min_val=1,
        max_val=9,
        default=max(1, int(requirements.total_duration/5)),
        state=state
    )

    # 确保转换为整数
    num_scenes = int(num_scenes)

    # 计算已使用的时间
    used_duration = 0

    for i in range(num_scenes):
        # 计算剩余时间
        remaining_time = requirements.total_duration - used_duration

        print(f"\n{'='*40}")
        print(f"📹 分镜头 {i+1}/{num_scenes}")
        if remaining_time > 0:
            print(f"⏱️ 剩余可用时间: {remaining_time} 秒")
        print("="*40)

        # 每次循环创建新的state用于这个分镜头
        scene_state = QuestionnaireState()
        scene_state.current_section = f"分镜头{i+1}"

        scene = Scene(
            index=i+1,
            duration=0,
            camera_angle="",
            description="",
            transition_to_next="直接切换"
        )

        # 1. 先问时长
        scene.duration = ask_numeric(
            f"  时长",
            f"  第 {i+1} 个分镜头持续多少秒？（剩余 {remaining_time} 秒）",
            min_val=0.5,
            max_val=remaining_time if remaining_time > 0 else requirements.total_duration,
            default=min(remaining_time / (num_scenes - i), 5) if i < num_scenes - 1 else remaining_time,
            state=scene_state,
            show_remaining=remaining_time
        )
        used_duration += scene.duration

        # 2. 先问场景描述（主要内容）
        scene.description = ask_with_ai(
            f"  场景描述",
            f"  详细描述第 {i+1} 个分镜头要展示什么内容",
            ai,
            context=requirements.overall_style,
            state=scene_state
        )

        # 3. 再问镜头机位（正面、侧面等），带通俗解释
        print(f"\n  📷 镜头机位指南（选择困难？看看通俗解释）:")

        # 显示通俗解释
        camera_guide = get_camera_guide()
        for angle, info in camera_guide.items():
            print(f"     {angle}: {info['通俗解释']} (情感: {info['情感']})")

        scene.camera_angle = ask_with_options_and_ai(
            f"  镜头机位",
            f"  使用什么角度的镜头拍摄这个场景？（见上方通俗指南）",
            [
                ("正面", "像和人面对面说话 - 表达真诚、直接"),
                ("侧面", "像在旁边看热闹 - 展示动作线条"),
                ("斜侧", "45度角自拍角度 - 最常用的上镜角度"),
                ("低角度", "蹲下来仰视 - 表现高大、权威"),
                ("高角度", "站高处往下看 - 展示全貌"),
                ("俯冲", "像老鹰俯冲 - 震撼开场"),
                ("升格", "慢慢升起来 - 希望升起、史诗感"),
                ("旋转", "绕着转圈 - 梦境、眩晕、浪漫")
            ],
            ai,
            requirements.theme,
            scene_state
        )

        # 如果选择了经典电影，显示对应的镜头建议
        if selected_film and i == 0:
            print(f"\n  💡 致敬大师建议: {selected_film['name']} 中的 {selected_film['camera_angle']} 镜头")
            print(f"     参考: {selected_film['reference']}")

        # 镜头组合建议
        print("\n  📽️ 镜头组合建议:")
        shot_combos = get_shot_combinations()
        combo_list = list(shot_combos.keys())
        for j, combo_name in enumerate(combo_list[:4], 1):
            print(f"     {j}. {combo_name}")
        print(f"     0. 暂时不需要")

        combo_choice = input(f"  选择镜头组合（直接回车跳过）: ").strip()
        if combo_choice.isdigit() and 0 < int(combo_choice) <= len(combo_list):
            selected_combo = shot_combos[combo_list[int(combo_choice) - 1]]
            print(f"\n  ✅ 已应用镜头组合: {combo_list[int(combo_choice) - 1]}")
            print(f"     {selected_combo['description']}")

        # 智能AI推荐（如果可用）
        if ai and ai.is_available():
            print("\n  🤖 需要 AI 智能推荐镜头吗？(y/n)")
            print("     AI 会根据你的场景描述，推荐最佳镜头")
            ai_choice = input("  > ").strip().lower()
            if ai_choice == "y":
                result = ai.suggest_smart_lens(
                    scene.description,
                    requirements.theme,
                    requirements.overall_style,
                    ""
                )
                if result and result.suggestions:
                    print("\n  📋 AI 镜头建议:")
                    print(f"  {result.suggestions[0]}")

        # 4. 过渡效果（最后一个分镜头不需要）
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
                requirements.theme,
                scene_state
            )

        requirements.scenes.append(scene)

    # 第六部分：素材
    print("\n🖼️ 第六部分：参考素材（可选）")
    print("-"*40)
    state.current_section = "参考素材"

    print("\n参考图片路径 (每行一个路径，直接回车结束):")
    try:
        while True:
            img = input("  > ").strip()
            if not img:
                break
            requirements.images.append(img)
    except EOFError:
        pass

    try:
        print("\n参考视频路径 (每行一个路径，直接回车结束):")
        while True:
            vid = input("  > ").strip()
            if not vid:
                break
            requirements.videos.append(vid)
    except EOFError:
        pass

    try:
        print("\n背景音乐路径 (每行一个路径，直接回车结束):")
        while True:
            aud = input("  > ").strip()
            if not aud:
                break
            requirements.audios.append(aud)
    except EOFError:
        pass

    return requirements


def ask_with_ai(question: str, help_text: str,
                ai: Optional[AIExtension] = None,
                context: str = "",
                state: Optional[QuestionnaireState] = None) -> str:
    """带 AI 辅助的问题"""
    while True:
        print(f"\n{question}")
        print(f"💡 {help_text}")
        print("💡 输入 'ai' 获取 AI 建议，输入 'b' 返回上一题")
        print("> ", end="")

        answer = input().strip()

        # 处理返回
        if answer.lower() == "b":
            if state and state.can_go_back():
                prev = state.go_back()
                if prev:
                    print(f"\n↩️ 已返回上一题: {prev['question']}")
                    print(f"上次的答案: {prev['answer']}")
                    # 这里可以实现重新输入或者直接使用上次的答案
                    continue
            else:
                print("⚠️ 无法返回，已经是第一步")
                continue

        # 如果用户输入 ai
        if answer.lower() == "ai":
            return get_ai_suggestion(question, help_text, ai, context)

        while not answer:
            print("⚠️ 请输入内容，或输入 'ai' 寻求 AI 帮助，输入 'b' 返回")
            print("> ", end="")
            answer = input().strip()
            if answer.lower() == "b":
                break
            if answer.lower() == "ai":
                return get_ai_suggestion(question, help_text, ai, context)

        if answer.lower() == "b":
            continue

        # 保存步骤
        if state:
            state.save_step(state.current_section, question, answer)

        return answer


def ask_with_options_and_ai(question: str, help_text: str,
                          options: List[tuple],
                          ai: Optional[AIExtension] = None,
                          context: str = "",
                          state: Optional[QuestionnaireState] = None,
                          default: str = "") -> str:
    """带选项和 AI 辅助的问题，支持输入校验"""
    while True:
        print(f"\n{question}")
        print(f"💡 {help_text}")

        # 显示选项
        print("\n可选值:")
        for i, (key, desc) in enumerate(options, 1):
            print(f"  {i}. {key} - {desc}")

        print("💡 输入数字选择，或输入 'ai' 获取 AI 建议")
        print("💡 输入 'b' 返回上一题")
        if default:
            print(f"💡 直接回车使用默认值: {default}")
        print("> ", end="")

        answer = input().strip()

        # 处理返回
        if answer.lower() == "b":
            if state and state.can_go_back():
                prev = state.go_back()
                if prev:
                    print(f"\n↩️ 已返回上一题")
                    continue
            else:
                print("⚠️ 无法返回，已经是第一步")
                continue

        # AI 建议
        if answer.lower() == "ai":
            return get_ai_suggestion_with_options(question, options, ai, context)

        # 数字选择
        if answer.isdigit():
            idx = int(answer) - 1
            if 0 <= idx < len(options):
                if state:
                    state.save_step(state.current_section, question, options[idx][0])
                return options[idx][0]

        # 默认值
        if not answer and default:
            if state:
                state.save_step(state.current_section, question, default)
            return default

        # 输入校验：检查是否输入了选项文字
        if answer:
            # 检查是否完全匹配某个选项
            matched = False
            for key, desc in options:
                if answer == key or answer.lower() == key.lower():
                    if state:
                        state.save_step(state.current_section, question, key)
                    return key

            # 如果不是有效选项，提示错误
            print("⚠️ 请输入有效的选项编号（1-{0}），或输入选项名称".format(len(options)))
            continue

        # 空输入且无默认值时重新循环
        print("⚠️ 请输入有效选项")


def ask_with_multiple_options(question: str, help_text: str,
                              options: List[tuple],
                              ai: Optional[AIExtension] = None,
                              context: str = "",
                              state: Optional[QuestionnaireState] = None,
                              default: str = "") -> str:
    """带选项的问题，支持多选"""
    while True:
        print(f"\n{question}")
        print(f"💡 {help_text}")

        # 显示选项
        print("\n可选值:")
        for i, (key, desc) in enumerate(options, 1):
            print(f"  {i}. {key} - {desc}")

        print("💡 输入数字多选（如：1,3,5 或 1-3），或输入 'ai' 获取 AI 建议")
        print("💡 输入 'b' 返回上一题")
        if default:
            print(f"💡 直接回车使用默认值: {default}")
        print("> ", end="")

        answer = input().strip()

        # 处理返回
        if answer.lower() == "b":
            if state and state.can_go_back():
                prev = state.go_back()
                if prev:
                    print(f"\n↩️ 已返回上一题")
                    continue
            else:
                print("⚠️ 无法返回，已经是第一步")
                continue

        # AI 建议
        if answer.lower() == "ai":
            return get_ai_suggestion_with_options(question, options, ai, context)

        # 解析多选
        selected = []
        if answer:
            # 处理逗号分隔或范围
            parts = answer.replace(",", " ").split()
            for part in parts:
                if "-" in part:
                    try:
                        start, end = map(int, part.split("-"))
                        selected.extend(range(start, end + 1))
                    except ValueError:
                        print("⚠️ 范围格式错误，请使用如 1-3 的格式")
                        break
                else:
                    try:
                        selected.append(int(part))
                    except ValueError:
                        print("⚠️ 输入格式错误，请使用如 1,3,5 或 1-3 的格式")
                        break
            else:
                # 验证所有选择是否有效
                valid = all(1 <= s <= len(options) for s in selected)
                if valid:
                    result = ", ".join(options[s-1][0] for s in selected)
                    if state:
                        state.save_step(state.current_section, question, result)
                    return result
                else:
                    print("⚠️ 请输入有效的选项编号（1-{0}）".format(len(options)))
                    continue
        else:
            # 默认值
            if default:
                if state:
                    state.save_step(state.current_section, question, default)
                return default
            print("⚠️ 请输入选项")


def ask_numeric(question: str, help_text: str,
               min_val: float = 1, max_val: float = 999,
               default: float = 0,
               state: Optional[QuestionnaireState] = None,
               show_remaining: float = None) -> float:
    """询问数值，支持返回和输入校验"""
    while True:
        print(f"\n{question}")
        if show_remaining is not None:
            print(f"💡 剩余可用时间: {show_remaining} 秒")
        print(f"💡 {help_text}")
        if default:
            print(f"💡 直接回车使用默认值: {default}")
        print("💡 输入 'b' 返回上一题")
        print(f"💡 请输入 {min_val}-{max_val} 之间的数值")
        print("> ", end="")

        answer = input().strip()

        # 处理返回
        if answer.lower() == "b":
            if state and state.can_go_back():
                prev = state.go_back()
                if prev:
                    print(f"\n↩️ 已返回上一题")
                    continue
            else:
                print("⚠️ 无法返回，已经是第一步")
                continue

        if not answer:
            if default:
                if state:
                    state.save_step(state.current_section, question, default)
                return default
            print("⚠️ 请输入数值")
            continue

        # 输入校验
        try:
            value = float(answer)
            if min_val <= value <= max_val:
                if state:
                    state.save_step(state.current_section, question, value)
                return value
            else:
                print(f"⚠️ 请输入 {min_val}-{max_val} 之间的数值")
        except ValueError:
            print("⚠️ 请输入有效数字")


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


if __name__ == "__main__":
    # 测试
    req = enhanced_questionnaire()
    from questionnaire import print_requirements
    print_requirements(req)
