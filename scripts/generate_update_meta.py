#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.8.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.8.0.apk"
    notes = (
        "• [급코스 드리프트 & 카빙 코너링 대폭 강화] S자 코너·헤어핀·능선 분기·결승 코너 곡률(±2.65~3.45)을 다이나믹한 급코너로 업그레이드하고, 드리프트 시 안쪽 에이펙스를 날카롭게 파고드는 카빙 그립과 3단 드리프트 부스트(청색·주황·보라) 완성!\n"
        "• [캐릭터 얼굴 크기 대폭 확대 (108x108 + 최대 2.85배)] 내 캐릭터(1.56배)와 라이벌 캐릭터(최대 2.85배)의 얼굴 컷아웃 크기를 대폭 키워 주행 중 누구의 얼굴인지 한눈에 선명하게 식별!\n"
        "• [상대편 AI 경쟁력 상향 & 투척·발사형 공격 아이템 5종 전면 개편] AI 주행 페이스(1.018~1.058) 및 코너 공략 속도를 높여 치열한 접전을 구현하고, 아이템을 주로 던지거나 쏘는 5종(🚀유도 로켓·💣왕폭탄 던지기·🐢3연발 등껍질·❄️얼음대포·🍌바나나 전방 투척)으로 전면 개편!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 17,
        "versionName": "1.8.0",
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
                "latest_version": "1.8.0",
                "version_code": 17,
                "force_update": False,
                "release_notes": "급코스 드리프트 카빙 물리, 캐릭터 얼굴 대폭 확대(108x108 + 최대 2.85배), 상대편 AI 속도·코너링 상향, 투척·발사형 공격 아이템 5종(유도로켓·왕폭탄·3연발등껍질·얼음대포·왕바나나투척) 및 자동 업데이트 개선 완성.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.8.0 (build 17), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
