# -*- coding: utf-8 -*-
"""
Seedance 2.0 API 客户端模块
"""

import json
import time
import hashlib
import os
from typing import Dict, Any, Optional, List
from dataclasses import asdict
import requests
from urllib.parse import urljoin


class SeedanceAPIError(Exception):
    """API 错误异常"""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"API Error {code}: {message}")


class SeedanceClient:
    """Seedance 2.0 API 客户端"""

    def __init__(self, base_url: str, api_key: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def generate_video(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        提交视频生成请求

        参数:
            params: 视频生成参数，包含:
                - theme: 主题
                - story: 故事描述
                - overall_style: 整体格调
                - overall_lighting: 整体光照
                - color_tone: 色调
                - lens_selection: 镜头选型
                - aspect_ratio: 屏幕比例
                - total_duration: 总时长
                - rhythm: 节奏
                - scenes: 分镜头列表
                - images: 参考图片
                - videos: 参考视频
                - audios: 背景音乐
        """
        endpoint = "/v1/video/generate"

        # 构建 API 请求参数
        api_params = self._build_request_params(params)

        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.post(url, json=api_params, timeout=self.timeout)
            response.raise_for_status()

            result = response.json()

            if result.get("code") != 0 and result.get("code") != 200:
                raise SeedanceAPIError(
                    result.get("code", -1),
                    result.get("message", "Unknown error")
                )

            return result

        except requests.exceptions.RequestException as e:
            raise SeedanceAPIError(-1, f"Network error: {str(e)}")

    def query_job(self, job_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        endpoint = f"/v1/video/query/{job_id}"

        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            raise SeedanceAPIError(-1, f"Network error: {str(e)}")

    def wait_for_completion(self, job_id: str, poll_interval: int = 5,
                           max_wait: int = 600) -> Dict[str, Any]:
        """等待任务完成"""
        start_time = time.time()

        while True:
            if time.time() - start_time > max_wait:
                raise SeedanceAPIError(-1, "Timeout waiting for video generation")

            result = self.query_job(job_id)

            status = result.get("data", {}).get("status", "")

            if status == "completed":
                return result
            elif status == "failed":
                raise SeedanceAPIError(-1, result.get("data", {}).get("error", "Generation failed"))
            elif status == "processing":
                print(f"⏳ 视频生成中... (已等待 {int(time.time() - start_time)} 秒)")
                time.sleep(poll_interval)
            else:
                print(f"📊 当前状态: {status}")
                time.sleep(poll_interval)

    def _build_request_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """构建 API 请求参数"""

        # 基础参数
        api_params = {
            "theme": params.get("theme", ""),
            "story": params.get("story", ""),
            "aspect_ratio": params.get("aspect_ratio", "16:9"),
            "duration": float(params.get("total_duration", 30)),
        }

        # 风格参数
        style_params = {
            "style": params.get("overall_style", ""),
            "lighting": params.get("overall_lighting", ""),
            "color_tone": params.get("color_tone", ""),
            "lens": params.get("lens_selection", ""),
            "rhythm": params.get("rhythm", ""),
        }
        api_params["style"] = style_params

        # 分镜头参数
        scenes = params.get("scenes", [])
        if scenes:
            api_params["scenes"] = []
            for scene in scenes:
                scene_data = {
                    "index": scene.get("index", 1),
                    "duration": scene.get("duration", 5),
                    "camera_angle": scene.get("camera_angle", ""),
                    "description": scene.get("description", ""),
                    "transition": scene.get("transition_to_next", "直接切换"),
                }
                api_params["scenes"].append(scene_data)

        # 素材参数
        if params.get("images"):
            api_params["images"] = params["images"]
        if params.get("videos"):
            api_params["videos"] = params["videos"]
        if params.get("audios"):
            api_params["audios"] = params["audios"]

        return api_params


def submit_video_request(client: SeedanceClient, requirements: Any) -> Dict[str, Any]:
    """提交视频生成请求"""

    print("\n" + "="*60)
    print("🚀 正在提交视频生成请求...")
    print("="*60)

    # 转换为字典
    params = requirements.to_dict() if hasattr(requirements, "to_dict") else requirements

    try:
        result = client.generate_video(params)

        if result.get("code") == 0 or result.get("code") == 200:
            job_id = result.get("data", {}).get("job_id", "")
            print(f"\n✅ 请求提交成功！")
            print(f"📋 任务 ID: {job_id}")
            print("\n⏳ 等待视频生成...")

            # 等待生成完成
            final_result = client.wait_for_completion(job_id)

            video_url = final_result.get("data", {}).get("video_url", "")
            if video_url:
                print(f"\n🎬 视频生成完成！")
                print(f"📎 视频地址: {video_url}")
            else:
                print(f"\n🎬 视频生成完成！")
                print(f"📋 结果: {json.dumps(final_result.get('data', {}), ensure_ascii=False, indent=2)}")

            return final_result
        else:
            error_msg = result.get("message", "Unknown error")
            print(f"\n❌ 请求失败: {error_msg}")
            return result

    except SeedanceAPIError as e:
        print(f"\n❌ API 错误: {e.message}")
        raise
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        raise


def test_api_connection(client: SeedanceClient) -> bool:
    """测试 API 连接"""
    try:
        # 尝试一个简单的查询来验证连接
        response = client.session.get(
            urljoin(client.base_url, "/v1/health"),
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False


if __name__ == "__main__":
    print("Seedance API 客户端测试")
    print("="*60)

    # 读取配置
    import yaml

    config_path = os.path.expanduser("~/.seedance_helper/config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        print("配置文件不存在，请先运行主程序生成配置")
        exit(1)

    # 创建客户端
    client = SeedanceClient(
        base_url=config["api"]["base_url"],
        api_key=config["api"]["api_key"]
    )

    print(f"API 地址: {client.base_url}")

    # 测试连接
    if test_api_connection(client):
        print("✅ API 连接正常")
    else:
        print("⚠️ API 连接失败，请检查配置")
