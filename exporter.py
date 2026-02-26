# -*- coding: utf-8 -*-
"""
JSON 导出器 - 生成符合 Seedance 2.0 API 格式的 JSON
"""

import json
import os
from typing import Dict, Any
from datetime import datetime


def export_to_seedance_json(requirements: Any, output_path: str = None) -> Dict[str, Any]:
    """
    导出为 Seedance 2.0 API 格式的 JSON

    参数:
        requirements: VideoRequirements 对象
        output_path: 输出文件路径（可选）

    返回:
        符合 Seedance 2.0 API 格式的字典
    """

    # 转换为字典
    if hasattr(requirements, "to_dict"):
        params = requirements.to_dict()
    else:
        params = requirements

    # 构建 Seedance 2.0 API 格式
    api_format = {
        "meta": {
            "version": "2.0",
            "exported_at": datetime.now().isoformat(),
            "generator": "Seedance Helper CLI"
        },
        "video": {
            "theme": params.get("theme", ""),
            "story": params.get("story", ""),
            "aspect_ratio": params.get("aspect_ratio", "16:9"),
            "duration": float(params.get("total_duration", 30)),
            "fps": 24,
            "quality": "high"
        },
        "style": {
            "overall_style": params.get("overall_style", ""),
            "lighting": params.get("overall_lighting", ""),
            "color_tone": params.get("color_tone", ""),
            "lens": params.get("lens_selection", ""),
            "rhythm": params.get("rhythm", "")
        },
        "scenes": [],
        "assets": {
            "images": [],
            "videos": [],
            "audios": []
        }
    }

    # 添加分镜头
    scenes = params.get("scenes", [])
    for scene in scenes:
        scene_data = {
            "index": scene.get("index", 1),
            "duration": scene.get("duration", 5),
            "camera_angle": scene.get("camera_angle", ""),
            "description": scene.get("description", ""),
            "transition": scene.get("transition_to_next", "直接切换")
        }
        api_format["scenes"].append(scene_data)

    # 添加素材
    if params.get("images"):
        for img in params["images"]:
            api_format["assets"]["images"].append({"path": img})
    if params.get("videos"):
        for vid in params["videos"]:
            api_format["assets"]["videos"].append({"path": vid})
    if params.get("audios"):
        for aud in params["audios"]:
            api_format["assets"]["audios"].append({"path": aud})

    # 如果指定了输出路径，保存到文件
    if output_path:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(api_format, f, ensure_ascii=False, indent=2)
        print(f"✅ 已导出 Seedance 2.0 格式到: {output_path}")

    return api_format


def print_json_preview(data: Dict[str, Any]):
    """打印 JSON 预览"""
    print("\n" + "="*60)
    print("📄 Seedance 2.0 JSON 预览")
    print("="*60)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("="*60)


def export_simple_json(requirements: Any, output_path: str = None) -> Dict[str, Any]:
    """
    导出为简化版的 JSON（更适合复制粘贴到其他平台）

    参数:
        requirements: VideoRequirements 对象
        output_path: 输出文件路径（可选）

    返回:
        简化版 JSON 字典
    """

    # 转换为字典
    if hasattr(requirements, "to_dict"):
        params = requirements.to_dict()
    else:
        params = requirements

    # 简化格式
    simple_format = {
        "theme": params.get("theme", ""),
        "story": params.get("story", ""),
        "aspect_ratio": params.get("aspect_ratio", "16:9"),
        "duration": params.get("total_duration", 30),
        "style": {
            "overall_style": params.get("overall_style", ""),
            "lighting": params.get("overall_lighting", ""),
            "color_tone": params.get("color_tone", ""),
            "lens_selection": params.get("lens_selection", ""),
            "rhythm": params.get("rhythm", "")
        },
        "scenes": []
    }

    # 添加分镜头
    scenes = params.get("scenes", [])
    for scene in scenes:
        simple_format["scenes"].append({
            "index": scene.get("index", 1),
            "duration": scene.get("duration", 5),
            "camera_angle": scene.get("camera_angle", ""),
            "description": scene.get("description", ""),
            "transition": scene.get("transition_to_next", "直接切换")
        })

    # 添加素材路径（简化）
    if params.get("images"):
        simple_format["images"] = params["images"]
    if params.get("videos"):
        simple_format["videos"] = params["videos"]
    if params.get("audios"):
        simple_format["audios"] = params["audios"]

    # 如果指定了输出路径，保存到文件
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(simple_format, f, ensure_ascii=False, indent=2)
        print(f"✅ 已导出到: {output_path}")

    return simple_format


if __name__ == "__main__":
    # 测试
    from questionnaire import VideoRequirements, Scene

    req = VideoRequirements()
    req.theme = "测试主题"
    req.story = "测试故事"
    req.overall_style = "电影感"
    req.overall_lighting = "自然光"
    req.color_tone = "暖色调"
    req.lens_selection = "广角镜头"
    req.aspect_ratio = "16:9"
    req.total_duration = 30
    req.rhythm = "快节奏"

    scene1 = Scene(
        index=1,
        duration=10,
        camera_angle="正面",
        description="开场镜头",
        transition_to_next="淡入淡出"
    )
    req.scenes.append(scene1)

    # 测试导出
    data = export_to_seedance_json(req)
    print_json_preview(data)
