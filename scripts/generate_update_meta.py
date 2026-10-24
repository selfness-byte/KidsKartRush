#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.3.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.3.apk"
    notes = (
        "• [선명하고 큼직한 얼굴 사진 (빅헤드 SD 포트레이트)] 📸 사진 촬영/업로드 시 얼굴 자동 인식 클로즈업(320px 고화질) 및 인게임 카트 위 얼굴 액자 크기를 2배 이상 키워 내 캐릭터와 라이벌 모두 누구인지 한눈에 알아보도록 개선!\n"
        "• [다이나믹 굴절코스 & 코너 갈매기 유도 표지판] 🛣️ 8개 전 코스에 S자 연속 굴절 시케인·90도 직각 코너·헤어핀 구간과 코너 방향 유도 표지판(Chevron Sign) 추가!\n"
        "• [드리프트 되듯이 미끄러지는 슬라이딩 효과] 🏎️💨 코너에서 차체가 사선으로 미끄러져 들어가는 리얼 슬립 물리, 아스팔트 2줄 타이어 스키드마크 자국 & 하얀 타이어 연기 연출!\n"
        "• [부스터 밸런스 조절] 🚀 과도했던 자동 부스터 및 대시패드 빈도를 줄이고, 코너 드리프트로 게이지를 모아 직접 터뜨리는 손맛 강화!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 9,
        "versionName": "1.5.3",
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
                "latest_version": "1.5.3",
                "version_code": 9,
                "force_update": False,
                "release_notes": "한눈에 알아보는 대형 고화질 얼굴 사진(빅헤드 SD 포트레이트), S자·헤어핀 굴절코스 추가, 코너에서 드리프트 되듯 미끄러지는 슬라이딩 물리·타이어 스키드마크 및 부스터 빈도 최적화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.3 (build 9), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
