# -*- coding: utf-8 -*-
"""
问答系统模块 - 收集视频创作需求
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Scene:
    """分镜头"""
    index: int
    duration: float  # 秒
    camera_angle: str  # 镜头机位
    description: str  # 分镜头描述
    transition_to_next: str  # 与下个镜头的过渡形式


@dataclass
class VideoRequirements:
    """视频需求完整数据"""
    # 整体风格
    overall_style: str = ""  # 整体格调
    overall_lighting: str = ""  # 整体光照
    color_tone: str = ""  # 色调

    # 镜头设置
    lens_selection: str = ""  # 镜头选型
    aspect_ratio: str = "16:9"  # 屏幕比例

    # 时间节奏
    total_duration: float = 0  # 总时长（秒）
    rhythm: str = ""  # 节奏描述

    # 分镜头列表
    scenes: List[Scene] = field(default_factory=list)

    # 主题/故事
    theme: str = ""  # 视频主题
    story: str = ""  # 故事描述

    # 额外素材
    images: List[str] = field(default_factory=list)  # 参考图片路径
    videos: List[str] = field(default_factory=list)  # 参考视频路径
    audios: List[str] = field(default_factory=list)  # 背景音乐

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = {
            "overall_style": self.overall_style,
            "overall_lighting": self.overall_lighting,
            "color_tone": self.color_tone,
            "lens_selection": self.lens_selection,
            "aspect_ratio": self.aspect_ratio,
            "total_duration": self.total_duration,
            "rhythm": self.rhythm,
            "theme": self.theme,
            "story": self.story,
            "images": self.images,
            "videos": self.videos,
            "audios": self.audios,
            "scenes": [asdict(s) for s in self.scenes]
        }
        return data


class Question:
    """问答题目"""

    def __init__(self, key: str, question: str, help_text: str = "",
                 options: Optional[List[str]] = None,
                 is_multiple: bool = False,
                 default: str = ""):
        self.key = key
        self.question = question
        self.help_text = help_text
        self.options = options or []
        self.is_multiple = is_multiple
        self.default = default

    def get_prompt(self) -> str:
        """获取显示的问题文本"""
        prompt = f"\n{'='*60}\n{self.question}\n{'='*60}"
        if self.help_text:
            prompt += f"\n💡 提示: {self.help_text}"
        if self.options:
            prompt += "\n可选值:"
            for i, opt in enumerate(self.options, 1):
                prompt += f"\n  {i}. {opt}"
        if self.default:
            prompt += f"\n(直接回车使用默认值: {self.default})"
        prompt += "\n> "
        return prompt


class Questionnaire:
    """问卷系统"""

    def __init__(self):
        self.questions = []
        self._init_questions()

    def _init_questions(self):
        """初始化所有问题"""

        # 主题与故事
        self.questions.extend([
            Question(
                key="theme",
                question="📝 视频主题/标题",
                help_text="你希望制作一个关于什么主题的视频？例如：城市夜景、自然风光、产品展示等",
            ),
            Question(
                key="story",
                question="📖 故事描述",
                help_text="描述你想讲述的故事或展示的内容，越详细越好",
            ),
        ])

        # 整体风格
        self.questions.extend([
            Question(
                key="overall_style",
                question="🎨 整体格调",
                help_text="你希望视频呈现什么样的风格？",
                options=[
                    "电影感 - 电影级的画面质感和叙事风格",
                    "纪录片风格 - 真实、客观的记录形式",
                    "时尚潮流 - 现代、炫酷的视觉风格",
                    "温馨治愈 - 温暖、柔和的氛围",
                    "赛博朋克 - 未来科技感",
                    "复古怀旧 - 怀旧、复古的色调",
                    "极简主义 - 简洁、干练的画面",
                    "自然清新 - 清爽、自然的视觉效果"
                ]
            ),
            Question(
                key="overall_lighting",
                question="💡 整体光照",
                help_text="你希望视频整体的光线效果是怎样的？",
                options=[
                    "自然光 - 模拟日光、月光等自然光源",
                    "柔光 - 柔和、均匀的布光",
                    "硬光 - 强烈对比的明暗效果",
                    "背光 - 逆光剪影效果",
                    "霓虹灯 - 赛博朋克风格的灯光",
                    "暖色调光 - 温馨的暖黄色调",
                    "冷色调光 - 清凉的冷蓝色调",
                    "戏剧性光影 - 强烈的明暗对比"
                ]
            ),
            Question(
                key="color_tone",
                question="🎭 色调",
                help_text="你希望视频整体呈现什么颜色倾向？",
                options=[
                    "中性灰 - 真实自然的色彩",
                    "暖色调 - 橙黄色系的温暖感",
                    "冷色调 - 蓝绿色系的冷峻感",
                    "高饱和度 - 鲜艳夺目的色彩",
                    "低饱和度 - 柔和淡雅的色调",
                    "黑白/单色 - 经典的黑白风格",
                    "电影调色 - 专业的电影色彩分级",
                    "复古色调 - 怀旧的色彩风格"
                ]
            ),
        ])

        # 镜头设置
        self.questions.extend([
            Question(
                key="lens_selection",
                question="📷 镜头选型",
                help_text="你希望使用什么类型的镜头效果？",
                options=[
                    "广角镜头 - 宽广的视野，适合风景",
                    "标准镜头 - 接近人眼视角，自然真实",
                    "长焦镜头 - 压缩空间，突出主体",
                    "微距镜头 - 拍摄微小细节",
                    "鱼眼镜头 - 夸张的透视效果",
                    "推拉镜头 - 动态的镜头运动",
                    "斯坦尼康 - 平滑的稳定运动",
                    "航拍镜头 - 俯瞰视角"
                ]
            ),
            Question(
                key="aspect_ratio",
                question="📐 屏幕比例",
                help_text="视频的宽高比是多少？",
                options=[
                    "16:9 - 标准横屏（最常用）",
                    "9:16 - 竖屏（短视频平台）",
                    "1:1 - 方形（社交媒体）",
                    "21:9 - 电影宽屏",
                    "4:3 - 传统电视比例"
                ],
                default="16:9"
            ),
        ])

        # 时间节奏
        self.questions.extend([
            Question(
                key="total_duration",
                question="⏱️ 视频总时长",
                help_text="你希望视频总时长是多少秒？",
                default="30"
            ),
            Question(
                key="rhythm",
                question="🎵 节奏",
                help_text="你希望视频的整体节奏是怎样的？",
                options=[
                    "快节奏 - 快速切换，充满活力",
                    "中节奏 - 平衡的叙事节奏",
                    "慢节奏 - 舒缓、从容的氛围",
                    "由慢到快 - 渐进式的节奏变化",
                    "由快到慢 - 渐入式的节奏变化",
                    "快慢交替 - 富有变化的节奏"
                ]
            ),
        ])

    def get_scene_questions(self, scene_index: int) -> List[Question]:
        """获取分镜头的问题列表"""
        return [
            Question(
                key=f"scene_{scene_index}_duration",
                question=f"📹 分镜头 {scene_index + 1} - 时长",
                help_text=f"第 {scene_index + 1} 个分镜头持续多少秒？",
                default="5"
            ),
            Question(
                key=f"scene_{scene_index}_camera_angle",
                question=f"📹 分镜头 {scene_index + 1} - 镜头机位",
                help_text="使用什么角度的镜头？",
                options=[
                    "正面 - 正面面对主体",
                    "侧面 - 90度侧拍",
                    "斜侧 - 45度角拍摄",
                    "低角度 - 仰视视角",
                    "高角度 - 俯视视角",
                    "俯冲 - 从高处冲向主体",
                    "升格 - 从低处升起的视角",
                    "旋转 - 环绕主体旋转"
                ]
            ),
            Question(
                key=f"scene_{scene_index}_description",
                question=f"📹 分镜头 {scene_index + 1} - 场景描述",
                help_text=f"详细描述第 {scene_index + 1} 个分镜头要展示什么内容"
            ),
            Question(
                key=f"scene_{scene_index}_transition",
                question=f"📹 分镜头 {scene_index + 1} - 过渡效果",
                help_text=f"这个镜头与下一个镜头之间如何过渡？",
                options=[
                    "直接切换 - 无过渡直接切换",
                    "淡入淡出 - 渐变过渡",
                    "交叉溶解 - 叠化效果",
                    "擦除 - 方向性过渡",
                    "缩放过渡 - 缩放效果连接",
                    "模糊过渡 - 虚化过渡",
                    "黑场过渡 - 通过黑场过渡",
                    "匹配剪辑 - 基于相似性过渡"
                ]
            ),
        ]

    def get_ai_extension_prompt(self, key: str, user_answer: str) -> str:
        """生成 AI 扩展提示"""
        prompts = {
            "overall_style": f"用户选择了视频风格: {user_answer}。请提供更多详细的风格描述和关键词，可以给出3-5个不同的风格选项供选择。",
            "overall_lighting": f"用户选择了光照: {user_answer}。请详细描述这种光照效果，可以给出3-5个变体选项。",
            "color_tone": f"用户选择了色调: {user_answer}。请提供具体的色彩参数建议，可以给出3-5个色调变体。",
            "lens_selection": f"用户选择了镜头: {user_answer}。请解释这种镜头的特点和适用场景。",
            "rhythm": f"用户选择了节奏: {user_answer}。请提供具体的节奏建议，比如每秒多少帧、镜头切换频率等。",
        }
        return prompts.get(key, f"用户对 {key} 的回答是: {user_answer}。请提供专业的建议和更多选项。")


def run_questionnaire() -> VideoRequirements:
    """运行问卷，返回收集到的需求"""
    questionnaire = Questionnaire()
    requirements = VideoRequirements()

    # 第一部分：基础信息
    print("\n" + "="*60)
    print("🎬 Seedance 2.0 视频生成助手")
    print("="*60)
    print("\n让我们开始创建你的视频！")
    print("="*60)

    # 收集问题答案
    for q in questionnaire.questions:
        while True:
            print(q.get_prompt())
            answer = input().strip()

            # 使用默认值
            if not answer and q.default:
                answer = q.default

            if answer:
                setattr(requirements, q.key, answer)
                break
            else:
                print("⚠️ 请输入内容，或输入 'ai' 寻求 AI 帮助")

    # 询问是否需要分镜头
    print("\n" + "="*60)
    print("📹 分镜头设置")
    print("="*60)

    # 估算需要多少个分镜头
    estimated_scenes = max(1, int(float(requirements.total_duration) / 5))
    print(f"根据总时长 {requirements.total_duration} 秒，建议分为 {estimated_scenes} 个分镜头")

    while True:
        print("\n请输入分镜头数量 (1-9):")
        print("(直接回车使用建议值)")
        print("> ", end="")
        num_scenes = input().strip()

        if not num_scenes:
            num_scenes = estimated_scenes
        else:
            try:
                num_scenes = int(num_scenes)
                if num_scenes < 1 or num_scenes > 9:
                    print("⚠️ 分镜头数量应在 1-9 之间")
                    continue
            except ValueError:
                print("⚠️ 请输入有效数字")
                continue
        break

    # 收集每个分镜头的信息
    for i in range(num_scenes):
        print(f"\n{'='*60}")
        print(f"设置分镜头 {i+1}/{num_scenes}")
        print("="*60)

        scene = Scene(
            index=i+1,
            duration=5.0,
            camera_angle="",
            description="",
            transition_to_next="直接切换"
        )

        questions = questionnaire.get_scene_questions(i)
        for q in questions:
            print(q.get_prompt())
            answer = input().strip()

            if not answer and q.default:
                answer = q.default

            if answer:
                if "duration" in q.key:
                    try:
                        scene.duration = float(answer)
                    except ValueError:
                        scene.duration = 5.0
                elif "camera_angle" in q.key:
                    scene.camera_angle = answer
                elif "description" in q.key:
                    scene.description = answer
                elif "transition" in q.key:
                    scene.transition_to_next = answer

        requirements.scenes.append(scene)

    # 询问素材
    print("\n" + "="*60)
    print("🖼️ 参考素材（可选）")
    print("="*60)

    print("\n参考图片路径 (每行一个路径，直接回车结束):")
    print("> ", end="")
    while True:
        img = input().strip()
        if not img:
            break
        requirements.images.append(img)

    print("\n参考视频路径 (每行一个路径，直接回车结束):")
    print("> ", end="")
    while True:
        vid = input().strip()
        if not vid:
            break
        requirements.videos.append(vid)

    print("\n背景音乐路径 (每行一个路径，直接回车结束):")
    print("> ", end="")
    while True:
        aud = input().strip()
        if not aud:
            break
        requirements.audios.append(aud)

    return requirements


def print_requirements(req: VideoRequirements):
    """打印收集到的需求摘要"""
    print("\n" + "="*60)
    print("📋 视频需求摘要")
    print("="*60)

    print(f"\n🎬 主题: {req.theme}")
    print(f"📖 故事: {req.story[:100]}..." if len(req.story) > 100 else f"📖 故事: {req.story}")

    print(f"\n🎨 整体格调: {req.overall_style}")
    print(f"💡 整体光照: {req.overall_lighting}")
    print(f"🎭 色调: {req.color_tone}")

    print(f"\n📷 镜头选型: {req.lens_selection}")
    print(f"📐 屏幕比例: {req.aspect_ratio}")
    print(f"⏱️ 总时长: {req.total_duration} 秒")
    print(f"🎵 节奏: {req.rhythm}")

    print(f"\n📹 分镜头 ({len(req.scenes)} 个):")
    for s in req.scenes:
        print(f"  镜头 {s.index}: {s.duration}秒 - {s.camera_angle}")
        print(f"    描述: {s.description[:50]}..." if len(s.description) > 50 else f"    描述: {s.description}")
        print(f"    过渡: {s.transition_to_next}")

    print(f"\n🖼️ 参考图片: {len(req.images)} 张")
    print(f"🎬 参考视频: {len(req.videos)} 个")
    print(f"🎵 背景音乐: {len(req.audios)} 首")

    print("\n" + "="*60)


if __name__ == "__main__":
    req = run_questionnaire()
    print_requirements(req)
