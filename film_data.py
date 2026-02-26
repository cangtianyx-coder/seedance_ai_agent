# -*- coding: utf-8 -*-
"""
电影镜头参考库与场景模板数据
为小白用户提供经典电影镜头参考和场景模板
"""

from typing import List, Dict, Any

# ============================================================
# 经典电影镜头参考库
# ============================================================
FILM_REFERENCE = {
    "盗梦空间": {
        "director": "克里斯托弗·诺兰",
        "description": "旋转镜头的经典代表",
        "reference": "酒店走廊失重旋转镜头",
        "tips": "适合表现梦境、眩晕感、时间错位",
        "camera_angle": "旋转",
        "style": "科幻"
    },
    "泰坦尼克号": {
        "director": "詹姆斯·卡梅隆",
        "description": "史诗级航拍与浪漫镜头",
        "reference": "从船舱到甲板的升降镜头",
        "tips": "适合表现宏大场景、浪漫氛围",
        "camera_angle": "升格",
        "style": "浪漫"
    },
    "荒野猎人": {
        "director": "亚利桑德罗·冈萨雷斯·伊纳里图",
        "description": "教科书级别的长镜头",
        "reference": "长镜头跟随主角战斗",
        "tips": "适合表现紧张追逐、一镜到底的流畅感",
        "camera_angle": "跟随",
        "style": "史诗"
    },
    "辛德勒的名单": {
        "director": "史蒂文·斯皮尔伯格",
        "description": "经典的黑白影像与红衣女孩",
        "reference": "红衣女孩在黑白人群中",
        "tips": "适合表现历史沉重感、对比强烈",
        "camera_angle": "高角度",
        "style": "历史"
    },
    "黑客帝国": {
        "director": "沃卓斯基兄弟",
        "description": "子弹时间的经典之作",
        "reference": "子弹穿过慢动作",
        "tips": "适合表现炫酷动作、科幻感",
        "camera_angle": "环绕",
        "style": "科幻"
    },
    "阿凡达": {
        "director": "詹姆斯·卡梅隆",
        "description": "开创性的3D航拍",
        "reference": "飞翔在潘多拉星球",
        "tips": "适合表现奇幻世界、自由飞翔",
        "camera_angle": "俯冲",
        "style": "奇幻"
    },
    "疯狂的石头": {
        "director": "宁浩",
        "description": "经典的多线叙事",
        "reference": "俯视视角的转场",
        "tips": "适合表现紧张幽默、复杂剧情",
        "camera_angle": "高角度",
        "style": "喜剧"
    },
    "让子弹飞": {
        "director": "姜文",
        "description": "独特的姜式暴力美学",
        "reference": "火车上的俯拍",
        "tips": "适合表现西部、英雄气概",
        "camera_angle": "斜侧",
        "style": "西部"
    },
    "英雄": {
        "director": "张艺谋",
        "description": "东方美学色彩运用",
        "reference": "秦军阵列的极简色彩",
        "tips": "适合表现史诗、历史、东方美学",
        "camera_angle": "正面",
        "style": "史诗"
    },
    "一代宗师": {
        "director": "王家卫",
        "description": "极致的光影与构图",
        "reference": "雨中对决的慢镜头",
        "tips": "适合表现武侠、情感、内敛",
        "camera_angle": "侧面",
        "style": "武侠"
    }
}

# ============================================================
# 场景模板库
# ============================================================
SCENE_TEMPLATES = {
    "日出日落": {
        "description": "适合表现时光流逝、情感变化",
        "scenes": [
            {"duration": 3, "camera_angle": "低角度", "description": "太阳从地平线升起/落下", "transition": "淡入淡出"},
            {"duration": 5, "camera_angle": "侧面", "description": "阳光勾勒出主体轮廓（剪影效果）", "transition": "交叉溶解"},
            {"duration": 4, "camera_angle": "正面", "description": "主体面向光源，温暖氛围", "transition": "直接切换"}
        ]
    },
    "城市夜景": {
        "description": "适合表现都市繁华、孤独感",
        "scenes": [
            {"duration": 4, "camera_angle": "高角度", "description": "城市灯火全景", "transition": "淡入淡出"},
            {"duration": 3, "camera_angle": "正面", "description": "霓虹灯闪烁的街道", "transition": "擦除"},
            {"duration": 5, "camera_angle": "侧面", "description": "车流光轨（长时间曝光效果）", "transition": "模糊过渡"},
            {"duration": 3, "camera_angle": "正面", "description": "孤独的主体走在街上", "transition": "直接切换"}
        ]
    },
    "海滩": {
        "description": "适合表现放松、自由、浪漫",
        "scenes": [
            {"duration": 4, "camera_angle": "高角度", "description": "海浪拍打沙滩全景", "transition": "淡入淡出"},
            {"duration": 4, "camera_angle": "低角度", "description": "海浪冲向镜头", "transition": "直接切换"},
            {"duration": 5, "camera_angle": "侧面", "description": "主体在沙滩行走", "transition": "交叉溶解"},
            {"duration": 2, "camera_angle": "正面", "description": "脚印在沙滩上", "transition": "匹配剪辑"}
        ]
    },
    "森林": {
        "description": "适合表现神秘、宁静、自然",
        "scenes": [
            {"duration": 5, "camera_angle": "高角度", "description": "阳光穿透树林", "transition": "淡入淡出"},
            {"duration": 4, "camera_angle": "正面", "description": "森林中的小径", "transition": "推拉镜头"},
            {"duration": 3, "camera_angle": "微距", "description": "树叶上的露珠/昆虫", "transition": "直接切换"},
            {"duration": 3, "camera_angle": "侧面", "description": "主体在林中穿行", "transition": "模糊过渡"}
        ]
    },
    "咖啡馆": {
        "description": "适合表现温馨、思考、相遇",
        "scenes": [
            {"duration": 3, "camera_angle": "斜侧", "description": "咖啡馆全景，窗边光线", "transition": "淡入淡出"},
            {"duration": 4, "camera_angle": "正面", "description": "咖啡杯冒出的热气", "transition": "直接切换"},
            {"duration": 5, "camera_angle": "侧面", "description": "人物在窗边思考/阅读", "transition": "交叉溶解"},
            {"duration": 3, "camera_angle": "特写", "description": "手指敲击键盘/搅拌咖啡", "transition": "匹配剪辑"}
        ]
    },
    "办公室": {
        "description": "适合表现职场、奋斗、压力",
        "scenes": [
            {"duration": 3, "camera_angle": "高角度", "description": "办公室全景", "transition": "淡入淡出"},
            {"duration": 4, "camera_angle": "正面", "description": "电脑屏幕/文件堆", "transition": "直接切换"},
            {"duration": 5, "camera_angle": "侧面", "description": "职员专注工作", "transition": "推拉镜头"},
            {"duration": 3, "camera_angle": "低角度", "description": "下班后空荡的办公室", "transition": "黑场过渡"}
        ]
    },
    "运动健身": {
        "description": "适合表现活力、汗水、坚持",
        "scenes": [
            {"duration": 2, "camera_angle": "高角度", "description": "健身房全景", "transition": "直接切换"},
            {"duration": 3, "camera_angle": "侧面", "description": "跑步机上的汗水", "transition": "直接切换"},
            {"duration": 4, "camera_angle": "正面", "description": "举铁/健身动作", "transition": "升格"},
            {"duration": 6, "camera_angle": "低角度", "description": "锻炼后的满足感", "transition": "淡入淡出"}
        ]
    },
    "家庭聚会": {
        "description": "适合表现温馨、欢乐、亲情",
        "scenes": [
            {"duration": 3, "camera_angle": "高角度", "description": "聚会全景", "transition": "淡入淡出"},
            {"duration": 4, "camera_angle": "正面", "description": "举杯庆祝", "transition": "直接切换"},
            {"duration": 4, "camera_angle": "侧面", "description": "交谈/欢笑", "transition": "交叉溶解"},
            {"duration": 4, "camera_angle": "正面", "description": "温馨合影", "transition": "淡入淡出"}
        ]
    }
}

# ============================================================
# 情绪板数据
# ============================================================
MOOD_BOARD = {
    "热血": {
        "keywords": ["激情", "奋斗", "拼搏", "梦想"],
        "style": "时尚潮流",
        "lighting": "硬光",
        "color_tone": "高饱和度",
        "rhythm": "快节奏",
        "description": "充满力量和激情，适合运动、励志类视频"
    },
    "温情": {
        "keywords": ["温暖", "感动", "治愈", "美好"],
        "style": "温馨治愈",
        "lighting": "柔光",
        "color_tone": "暖色调",
        "rhythm": "慢节奏",
        "description": "温暖人心的情感，适合家庭、爱情类视频"
    },
    "悬疑": {
        "keywords": ["紧张", "神秘", "未知", "恐惧"],
        "style": "电影感",
        "lighting": "背光",
        "color_tone": "冷色调",
        "rhythm": "由慢到快",
        "description": "紧张刺激的氛围，适合悬疑、恐怖类视频"
    },
    "浪漫": {
        "keywords": ["甜蜜", "美好", "永恒", "承诺"],
        "style": "电影感",
        "lighting": "柔光",
        "color_tone": "暖色调",
        "rhythm": "慢节奏",
        "description": "甜蜜温馨的爱情氛围"
    },
    "紧张": {
        "keywords": ["刺激", "危险", "紧迫", "对抗"],
        "style": "电影感",
        "lighting": "硬光",
        "color_tone": "低饱和度",
        "rhythm": "快节奏",
        "description": "紧张刺激的动作场景"
    },
    "怀旧": {
        "keywords": ["回忆", "过去", "时光", "思念"],
        "style": "复古怀旧",
        "lighting": "柔光",
        "color_tone": "复古色调",
        "rhythm": "慢节奏",
        "description": "回忆过去时光的情感"
    },
    "科技": {
        "keywords": ["未来", "智能", "冰冷", "精密"],
        "style": "赛博朋克",
        "lighting": "霓虹灯",
        "color_tone": "冷色调",
        "rhythm": "快节奏",
        "description": "未来科技感的视觉风格"
    },
    "自然": {
        "keywords": ["清新", "舒适", "放松", "原始"],
        "style": "自然清新",
        "lighting": "自然光",
        "color_tone": "中性灰",
        "rhythm": "中节奏",
        "description": "自然舒适的视觉体验"
    }
}

# ============================================================
# 镜头语言指南（更通俗的解释）
# ============================================================
CAMERA_GUIDE = {
    "正面": {
        "通俗解释": "就像和人面对面说话",
        "适用场景": "表达真诚、权威、对话",
        "经典案例": "新闻主播、领导人讲话",
        "情感": "直接、真诚、严肃"
    },
    "侧面": {
        "通俗解释": "像在旁边看热闹",
        "适用场景": "展示动作线条、轮廓",
        "经典案例": "走路、跑步、侧面肖像",
        "情感": "客观、冷静、观察"
    },
    "斜侧": {
        "通俗解释": "45度角自拍的角度",
        "适用场景": "最常用的上镜角度",
        "经典案例": "人物访谈、产品展示",
        "情感": "立体感、自然"
    },
    "低角度": {
        "通俗解释": "蹲下来仰视",
        "适用场景": "表现高大、权威、仰望",
        "经典案例": "英雄出场、建筑物",
        "情感": "尊敬、崇拜、压迫感"
    },
    "高角度": {
        "通俗解释": "站高处往下看",
        "适用场景": "展示全貌、弱势一方",
        "经典案例": "航拍城市、审判场景",
        "情感": "上帝视角、怜悯、渺小"
    },
    "俯冲": {
        "通俗解释": "像老鹰俯冲下来的感觉",
        "适用场景": "震撼开场、戏剧冲突",
        "经典案例": "动作片开场、极限运动",
        "情感": "冲击感、紧张、兴奋"
    },
    "升格": {
        "通俗解释": "慢慢升起来，像太阳升起",
        "适用场景": "英雄登场、希望升起",
        "经典案例": "领袖演讲、史诗开场",
        "情感": "希望、崇高、史诗感"
    },
    "旋转": {
        "通俗解释": "绕着主体转圈",
        "适用场景": "梦境、眩晕、浪漫",
        "经典案例": "盗梦空间、泰坦尼克号",
        "情感": "眩晕、浪漫、神秘"
    }
}

# ============================================================
# 镜头组合建议
# ============================================================
SHOT_COMBINATIONS = {
    "运动场景": {
        "description": "适合动作片、运动类视频",
        "sequence": [
            {"camera_angle": "高角度", "duration": 3, "description": "远景展示整个运动场地"},
            {"camera_angle": "正面", "duration": 2, "description": "运动员做准备"},
            {"camera_angle": "侧面", "duration": 4, "description": "运动过程"},
            {"camera_angle": "正面", "duration": 2, "description": "冲刺/爆发"},
            {"camera_angle": "低角度", "duration": 3, "description": "胜利/结束"}
        ],
        "transition": "快节奏切换"
    },
    "对话场景": {
        "description": "适合两人对话、访谈",
        "sequence": [
            {"camera_angle": "正面", "duration": 3, "description": "建立镜头（全景）"},
            {"camera_angle": "斜侧", "duration": 5, "description": "人物A说话（过肩镜头）"},
            {"camera_angle": "斜侧", "duration": 5, "description": "人物B反应（过肩镜头）"},
            {"camera_angle": "正面", "duration": 3, "description": "双方交流"},
            {"camera_angle": "特写", "duration": 2, "description": "关键表情/道具"}
        ],
        "transition": "直接切换"
    },
    "展示产品": {
        "description": "适合电商、产品展示",
        "sequence": [
            {"camera_angle": "高角度", "duration": 3, "description": "产品全景"},
            {"camera_angle": "正面", "duration": 4, "description": "产品正面展示"},
            {"camera_angle": "侧面", "duration": 3, "description": "侧面细节"},
            {"camera_angle": "微距", "duration": 5, "description": "特写细节"},
            {"camera_angle": "旋转", "duration": 4, "description": "360度展示"}
        ],
        "transition": "缩放过渡"
    },
    "旅行Vlog": {
        "description": "适合旅行记录、生活分享",
        "sequence": [
            {"camera_angle": "高角度", "duration": 4, "description": "目的地全景"},
            {"camera_angle": "正面", "duration": 3, "description": "到达时的表情"},
            {"camera_angle": "侧面", "duration": 5, "description": "探索过程"},
            {"camera_angle": "低角度", "duration": 3, "description": "有趣发现"},
            {"camera_angle": "正面", "duration": 5, "description": "感言/总结"}
        ],
        "transition": "交叉溶解"
    },
    "情感回忆": {
        "description": "适合怀旧、爱情、亲情",
        "sequence": [
            {"camera_angle": "高角度", "duration": 4, "description": "远景建立环境"},
            {"camera_angle": "侧面", "duration": 6, "description": "主体沉思/回忆"},
            {"camera_angle": "正面", "duration": 5, "description": "特写面部表情"},
            {"camera_angle": "升格", "duration": 4, "description": "升华/希望"},
            {"camera_angle": "正面", "duration": 3, "description": "收尾"}
        ],
        "transition": "淡入淡出"
    },
    "开场": {
        "description": "视频开场定调",
        "sequence": [
            {"camera_angle": "高角度", "duration": 5, "description": "大远景建立世界"},
            {"camera_angle": "俯冲", "duration": 3, "description": "快速接近主体"},
            {"camera_angle": "正面", "duration": 4, "description": "主体亮相"}
        ],
        "transition": "模糊过渡"
    }
}

# ============================================================
# 帮助函数
# ============================================================

def get_film_references() -> List[Dict[str, Any]]:
    """获取所有电影参考"""
    return [
        {"name": name, **info}
        for name, info in FILM_REFERENCE.items()
    ]

def get_scene_templates() -> Dict[str, Any]:
    """获取场景模板"""
    return SCENE_TEMPLATES

def get_mood_board() -> Dict[str, Any]:
    """获取情绪板"""
    return MOOD_BOARD

def get_camera_guide() -> Dict[str, Any]:
    """获取镜头指南"""
    return CAMERA_GUIDE

def get_shot_combinations() -> Dict[str, Any]:
    """获取镜头组合"""
    return SHOT_COMBINATIONS


if __name__ == "__main__":
    # 测试
    print("电影参考库测试:")
    for f in get_film_references()[:3]:
        print(f"  - {f['name']}: {f['description']}")

    print("\n场景模板测试:")
    for s in get_scene_templates().keys():
        print(f"  - {s}")

    print("\n情绪板测试:")
    for m in get_mood_board().keys():
        print(f"  - {m}")

    print("\n镜头组合测试:")
    for c in get_shot_combinations().keys():
        print(f"  - {c}")
