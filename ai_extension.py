# -*- coding: utf-8 -*-
"""
AI 扩展模块 - 帮助用户完善回答
"""

import json
import sys
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class AIExtensionResult:
    """AI 扩展结果"""
    suggestions: List[str]
    explanation: str
    keywords: List[str]


class AIExtension:
    """AI 扩展功能"""

    def __init__(self, api_key: str, model: str = "gpt-4", base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.client = None

        # 延迟导入，以便在无 API 密钥时也能运行
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        except ImportError:
            print("⚠️ 未安装 openai 库，AI 扩展功能不可用")
        except Exception as e:
            print(f"⚠️ AI 客户端初始化失败: {e}")

    def is_available(self) -> bool:
        """检查 AI 功能是否可用"""
        return self.client is not None

    def generate_suggestions(self, context: str, question: str, user_answer: str = "") -> Optional[AIExtensionResult]:
        """生成扩展建议"""
        if not self.is_available():
            return None

        system_prompt = """你是一位专业的视频制作顾问和创意导演。
根据用户正在创建的视频项目，提供专业的建议和多个选项供用户选择。

请根据以下规则生成回复：
1. 提供 3-5 个具体的选项建议选项都要有简
2. 每个短的解释
3. 使用的语言要简洁明了
4. 返回 JSON 格式的结果

JSON 格式：
{
    "suggestions": ["选项1 - 描述", "选项2 - 描述", ...],
    "explanation": "整体解释和建议",
    "keywords": ["关键词1", "关键词2", ...]
}"""

        user_prompt = f"""视频项目背景：
{context}

当前问题：
{question}

用户当前的回答：{user_answer if user_answer else '用户尚未回答'}

请提供专业的建议和更多选项。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content
            # 尝试解析 JSON
            try:
                # 尝试提取 JSON 部分
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]

                data = json.loads(content.strip())
                return AIExtensionResult(
                    suggestions=data.get("suggestions", []),
                    explanation=data.get("explanation", ""),
                    keywords=data.get("keywords", [])
                )
            except json.JSONDecodeError:
                # 如果 JSON 解析失败，返回原始内容
                return AIExtensionResult(
                    suggestions=[content],
                    explanation="",
                    keywords=[]
                )

        except Exception as e:
            print(f"⚠️ AI 请求失败: {e}")
            return None

    def expand_scene_description(self, scene_description: str, theme: str, style: str) -> Optional[str]:
        """扩展分镜头描述"""
        if not self.is_available():
            return None

        system_prompt = """你是一位专业的影视编剧和分镜头脚本作家。
根据用户提供的简短分镜头描述，将其扩展为详细的、可用于视频生成的分镜头脚本。

请提供：
1. 详细的环境描述
2. 主体动作描述
3. 镜头运动建议
4. 光线氛围描述

保持简洁，每个部分 1-2 句话。"""

        user_prompt = f"""视频主题：{theme}
整体风格：{style}
原始描述：{scene_description}

请扩展这个分镜头描述。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ AI 请求失败: {e}")
            return None

    def suggest_transitions(self, current_scene: str, next_scene: str) -> Optional[List[str]]:
        """建议过渡效果"""
        if not self.is_available():
            return None

        system_prompt = """你是一位专业的视频剪辑师。
根据前后两个分镜头的特点，推荐最适合的过渡效果。

请从以下选项中选择或推荐：
- 直接切换
- 淡入淡出
- 交叉溶解
- 擦除
- 缩放过渡
- 模糊过渡
- 黑场过渡
- 匹配剪辑

返回 2-3 个推荐选项，并简述理由。"""

        user_prompt = f"""当前镜头：{current_scene}
下一个镜头：{next_scene}

推荐哪些过渡效果？"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            return [response.choices[0].message.content]

        except Exception as e:
            print(f"⚠️ AI 请求失败: {e}")
            return None


def interactive_ai_help(ai: AIExtension, question_key: str, question_text: str,
                         user_answer: str = "", theme: str = "") -> Optional[str]:
    """交互式 AI 帮助"""
    if not ai.is_available():
        print("\n⚠️ AI 扩展功能不可用，请检查配置文件中的 API 密钥")
        return None

    # 根据问题类型构建上下文
    context_map = {
        "overall_style": f"视频主题：{theme}",
        "overall_lighting": f"视频主题：{theme}",
        "color_tone": f"视频主题：{theme}",
        "lens_selection": f"视频主题：{theme}",
        "rhythm": f"视频主题：{theme}",
    }

    context = context_map.get(question_key, f"视频主题：{theme}")

    print("\n🤖 正在请求 AI 助手帮助...")
    print("="*60)

    result = ai.generate_suggestions(context, question_text, user_answer)

    if result:
        print(f"\n📋 {result.explanation}\n" if result.explanation else "")

        if result.suggestions:
            print("💡 推荐选项:")
            for i, suggestion in enumerate(result.suggestions, 1):
                print(f"   {i}. {suggestion}")

        if result.keywords:
            print(f"\n🔑 关键词: {', '.join(result.keywords)}")

        print("\n" + "="*60)
        print("请选择上述选项的编号（输入数字），或者输入你自己的想法：")
        print("> ", end="")

        choice = input().strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(result.suggestions):
                # 提取选项内容
                selected = result.suggestions[idx]
                # 提取选项名称（去掉描述部分）
                return selected.split(" - ")[0] if " - " in selected else selected

        return choice if choice else None

    return None


def demo_ai_suggestions():
    """演示 AI 建议（当没有 API 密钥时）"""

    demo_suggestions = {
        "overall_style": [
            "电影感 - 电影级的画面质感和叙事风格，适合追求视觉冲击力的作品",
            "纪录片风格 - 真实、客观的记录形式，给人可信感",
            "时尚潮流 - 现代、炫酷的视觉风格，适合年轻人群体",
            "温馨治愈 - 温暖、柔和的氛围，让人感到舒适放松"
        ],
        "overall_lighting": [
            "自然光 - 模拟日光、月光等自然光源，营造真实感",
            "柔光 - 柔和、均匀的布光，适合人物和產品展示",
            "硬光 - 强烈对比的明暗效果，增加戏剧性",
            "背光 - 逆光剪影效果，营造神秘感"
        ],
        "color_tone": [
            "暖色调 - 橙黄色系的温暖感，适合温馨场景",
            "冷色调 - 蓝绿色系的冷峻感，适合科技感",
            "高饱和度 - 鲜艳夺目的色彩，充满活力",
            "电影调色 - 专业的电影色彩分级"
        ],
        "lens_selection": [
            "广角镜头 - 宽广的视野，适合风景和建筑",
            "标准镜头 - 接近人眼视角，自然真实",
            "长焦镜头 - 压缩空间，突出主体",
            "斯坦尼康 - 平滑的稳定运动镜头"
        ],
        "rhythm": [
            "快节奏 - 快速切换，每1-3秒切换镜头",
            "中节奏 - 平衡叙事，每4-6秒切换镜头",
            "慢节奏 - 舒缓氛围，每7-10秒切换镜头",
            "由慢到快 - 渐进式节奏变化"
        ]
    }

    return demo_suggestions


if __name__ == "__main__":
    print("AI 扩展模块测试")
    print("="*60)

    # 测试演示模式
    suggestions = demo_ai_suggestions()
    print("\n示例建议 - 整体格调:")
    for i, s in enumerate(suggestions["overall_style"], 1):
        print(f"  {i}. {s}")
