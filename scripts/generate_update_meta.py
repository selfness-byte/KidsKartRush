#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.0.apk"
    notes = (
        "• [상대편 선행 출발 & 하드코어 AI 난이도 대폭 상향] 상대 카트 5대가 출발부터 플레이어 앞으로 치고 나가며(초기 6위 출발), 주행 페이스(1.125~1.185)와 추월 가속(1.16~1.24 + N2O 부스트)을 대폭 강화해 끝까지 긴장감 넘치는 추격전 완성!\n"
        "• [전방 총격전 시스템 (앞에서 상대가 총을 쏘고 & 내 카트 기본 기관총 + 중화기 5종 사격)] 앞서 달리는 상대들이 전방에서 플레이어를 향해 기관총탄·레이저탄(조준 경고선 표시)을 발사하며, 내 카트도 프론트 트윈 개틀링건으로 상시 3점사 사격 및 5종 중화기(🔫개틀링 6연사·⚡플라즈마 스나이퍼·❄️아이스 산탄총·🚀유도 미사일·💣바주카 유탄포)로 맞대응!\n"
        "• [드리프트 '끼이익~!' 리얼 타이어 마찰 효과음 완성] 바람 소리 대신 고주파 포먼트 공명(1.6~2.4kHz) 듀얼 오실레이터와 스틱-슬립 마찰 비브라토를 결합해, 드리프트 진입·유지·탈출 시 아스팔트에 타이어가 날카롭게 미끄러지는 '끼이익~!' 스키드 사운드를 선명하게 구현!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 18,
        "versionName": "1.9.0",
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
                "latest_version": "1.9.0",
                "version_code": 18,
                "force_update": False,
                "release_notes": "상대편 전방 선행 및 하드코어 난이도 상향, 전방 총격전 시스템(상대 전방 사격 & 내 카트 상시 기관총 + 5종 중화기 총격), 드리프트 시 '끼이익~!' 리얼 타이어 스키드 효과음 적용.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.0 (build 18), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
