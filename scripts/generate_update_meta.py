#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.1.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.1.apk"
    notes = (
        "• [정통 3D 1/Z 원근감 극대화] 🛣️ 화면 하단 광폭 전경 도로에서 지평선 소실점까지 깊게 뻗어 나가는 정통 3D 핀홀 카메라 원근 투영(1/Z Perspective) 적용!\n"
        "• [입체 깊이 디테일] ✨ 도로 양옆 3D 반사봉(Delinator Posts), 입체 연석 베벨, 원거리 대기 원근 안개(Depth Fog), 코너 회전 시 2층 산맥·구름 시차(Parallax) 이동 적용\n"
        "• [리얼 원근 스케일링] 🏎️ 멀리 있는 라이벌 카트·아이템·가로수가 지평선 점 크기에서 내 차 크기까지 정확한 3D 거리 비율로 커지도록 개선\n"
        "• [얼굴 사진 & 1:1 직관 조작] 📸 내 캐릭터 및 모든 라이벌 머리 얼굴 사진 업로드, 지면 밀착형 흔들림 없는 카트, 1:1 직관적 핸들 조향 지원!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 7,
        "versionName": "1.5.1",
        "apkUrl": apk_url,
        "sha256": sha256,
        "sizeBytes": size_bytes,
        "updatedAt": "2026-10-24",
        "notes": notes,
    }

    targets = [
        PROJECT_DIR / "dist" / "update.json",
        Path("/Volumes/M/firebase-app-update-server/public/kidskart/update.json"),
        Path("/Volumes/M/inanimals-corp-website/public/kidskart/update.json"),
    ]
    for t in targets:
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(json.dumps(update_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # version.json 업데이트
    version_files = [
        Path("/Volumes/M/firebase-app-update-server/public/version.json"),
        Path("/Volumes/M/inanimals-corp-website/public/version.json"),
    ]
    for vf in version_files:
        if vf.exists():
            vdata = json.loads(vf.read_text(encoding="utf-8"))
            vdata.setdefault("apps", {})["com.mj.kidskart"] = {
                "app_name": "키즈 카트 러쉬!",
                "latest_version": "1.5.1",
                "version_code": 7,
                "force_update": False,
                "release_notes": "정통 3D 핀홀 카메라 1/Z 원근 투영(깊은 소실점·대기 원근감·3D 반사봉·2층 산맥 시차), 모든 레이서 머리 얼굴 사진 업로드, 지면 밀착 3D 카트 및 1:1 직관적 핸들 조작.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.1 (build 7), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
