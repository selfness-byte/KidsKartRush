#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.5.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.5.apk"
    notes = (
        "• [전방 적 군단 & 거대 보스 상시 전방 유지 물리 고도화!] ① 부스터·슈퍼부스트·스타·지름길 주행 중에도 적 전투 편대(👾드론 · 🏍️바이커 · 🛡️메카탱크)와 3단계 거대 보스(🤖아이언 스콜피온 · 🛸네온 디스트로이어 · 🐉메카 드래곤)가 플레이어 뒤로 밀려나지 않고 100% 항상 플레이어 전방 사격 거리(115m ~ 485m 앞)에서 앞서 달리며 치열한 전방 총격전을 펼치도록 개선, ② 보스 격파 직후 다음 스테이지 거대 보스가 0.85초 만에 즉시 전방에 출현하여 상시 보스 배틀 유지!\n"
        "• [전방 적 군단(3종) & 3단계 거대 보스전(Giant Boss Battle) 시스템] 상단 실시간 보스 HP 게이지 바, 3D 예광탄 궤적 광선, 황동 탄피 배출, 연사 손맛 및 3-Layer 탄도 사운드 적용!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 23,
        "versionName": "1.9.5",
        "apkUrl": apk_url,
        "sha256": sha256,
        "sizeBytes": size_bytes,
        "updatedAt": "2026-10-25",
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
                "app_name": "에어로 카트 GP: 선셋 캐니언 에디션",
                "latest_version": "1.9.5",
                "version_code": 23,
                "force_update": False,
                "release_notes": "적 전투 편대(드론·바이커·메카탱크)와 3단계 거대 보스가 항상 플레이어 전방(앞쪽)에서 앞서 달리며 총격전을 유지하도록 개선.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.5 (build 23), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
