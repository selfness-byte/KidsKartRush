#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.8.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.8.apk"
    notes = (
        "• [얼굴 UI 테두리·액자 완전 제거 & 얼굴만 재미있게 코믹 표현] 😄 로비 카드·사진 스튜디오·카트 위 캐릭터 머리에서 원형 테두리 선, 헬멧 림, 배경 액자를 100% 없애고, 통통한 볼살과 귀가 살아있는 '얼굴 전용 실루엣 컷아웃'으로 표현!\n"
        "• [살아 움직이는 코믹 보블헤드(Bobblehead) & 리액션 연출] 조향·드리프트·부스터에 따라 얼굴이 말랑말랑하게 통통 튀고 갸우뚱거리며, 발그레해지는 볼터치·부스터 반짝이(✨)·드리프트 스파크(⚡/💦) 등 익살스러운 표정 리액션 탑재!\n"
        "• [카트라이더 정통 드리프트 & 여성 음성 완전 제거 유지] 핸들 드리프트 끌기·카운터 스티어링 순부 점화 및 순수 V8 엔진·타이어 마찰음 사운드 적용!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 14,
        "versionName": "1.5.8",
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
                "app_name": "키즈 카트 러쉬!",
                "latest_version": "1.5.8",
                "version_code": 14,
                "force_update": False,
                "release_notes": "얼굴 나오는 모든 UI 및 카트 캐릭터 헤드에서 테두리·헬멧 액자를 완전히 제거하고, 통통한 얼굴 실루엣 컷아웃과 말랑말랑 보블헤드 탄성·코믹 홍조 리액션으로 재미있게 표현.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.8 (build 14), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
