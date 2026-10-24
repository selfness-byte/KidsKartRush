#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.2.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.2.0.apk"
    notes = (
        "• [신규] 🍄 슈퍼마리오 카트 & 카트라이더 러쉬+ 하이브리드 대개편 (마리오 서킷·레인보우 우주 로드·쿠파 용암 캐슬·요시 공룡 정글 4대 테마 트랙)\n"
        "• [신규] 🤸 점프(Hop) & 무지개 점프대 공중 트릭 액션, 3단 드리프트 스파크(파란불→주황불→보라불 미니터보), 자유로운 와이드 서스펜션 차체 물리 적용\n"
        "• [신규] ⭐ 슈퍼스타 무적 질주, 🍄 황금 거대버섯, 🚀 킬러 로켓 변신, 🐢 등껍질 발사, 🍌 바나나 껍질, ⚡ 번개 등 마리오 카트 슬롯 룰렛 아이템 탑재\n"
        "• [개선] 🏎️ 60fps 연속 깊이 투영 및 뒤에서 부스터로 치고 올라와 앞뒤로 엎치락뒤치락 추월하는 독립 물리 라이벌 AI & 후방 추월 경보 미러\n"
        "• [개선] 🔊 중저음 서브베이스(40~90Hz) + 트윈터보 디스토션이 결합된 묵직하고 두꺼운 슈퍼 부스터 사운드 & 앱 종료/백그라운드 시 사운드 즉시 차단"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 3,
        "versionName": "1.2.0",
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
                "latest_version": "1.2.0",
                "version_code": 3,
                "force_update": False,
                "release_notes": "슈퍼마리오 카트 & 카트라이더 러쉬+ 하이브리드 대개편! 점프대 공중 트릭, 3단 드리프트 미니터보, 마리오 카트 슬롯 아이템(슈퍼스타·황금버섯·킬러로켓·등껍질·바나나), 60fps 앞뒤 추월 라이벌 AI, 중저음 서브베이스 슈퍼부스터 사운드, 백그라운드 사운드 즉시 차단 적용.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.2.0 (build 3), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
