#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.3.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.3.0.apk"
    notes = (
        "• [삭제] 🚫 코너 도우미 버튼 및 자동 조향 개입 완전 삭제 (100% 직관적이고 자유로운 핸들 조작)\n"
        "• [디자인] 🧸 파스텔 장난감 캡슐 & 3D 젤리 버튼 스타일로 로비·HUD·핸들·아이템/부스터 버튼 UI가 훨씬 더 아기자기하고 귀엽게 업그레이드!\n"
        "• [그래픽] 🏎️ 3D 다층 시차(Yaw Parallax) 입체 카트 렌더링: 조향 각도에 따라 꺾이는 앞바퀴·노즈콘, 3D 원통형 광폭 타이어&휠 림, 입체 사이드 포드, 운전석 핸들 잡은 양손, 3D 리어 스포일러 윙, 구체 광택 헬멧 적용\n"
        "• [사운드] 🔊 경박한 고음 반복음을 완전히 제거하고, 중후하고 부드러운 저음 V8 배기음(36~110Hz) + 서브베이스 + 도로 주행 풍절음으로 고급스러운 주행 사운드 구현"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 4,
        "versionName": "1.3.0",
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
                "latest_version": "1.3.0",
                "version_code": 4,
                "force_update": False,
                "release_notes": "코너 도우미 완전 삭제, 파스텔 장난감 캡슐 & 3D 젤리 버튼 귀여운 UI 개편, 3D 다층 시차 입체 카트 그래픽 업그레이드, 경박한 고음을 제거한 중후하고 부드러운 저음 V8 배기음 적용.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.3.0 (build 4), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
