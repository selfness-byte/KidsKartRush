#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.5.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.5.apk"
    notes = (
        "• [장애물 vs 아이템 시각 구분 100% 명확화] ⚠️ 피해야 하는 모든 장애물(토관·바나나·오일·꽃게·얼음블록·가시바위알·쿵쿵이) 바닥에 빨간·노란 위험 경고 존(Red Danger Zone)과 머리 위 빨간 삼각형 '!' 경고 표지판을 띄우고, 먹는 아이템(무지개 '?' 박스·3D 회전 코인)은 시안·황금 빛기둥 오라로 한눈에 구분!\n"
        "• [8대 코스 다층 파노라마 랜드마크 배경 대폭 강화] 🏰 피치 성·거대 도넛산·해안 등대와 요트·오로라와 얼음궁전·화산과 브라키오 공룡·대관람차·쿠파 마왕성·은하수 유성우 및 하늘의 레이싱 비행선·열기구·2겹 응원 깃발 추가!\n"
        "• [역동적인 3D 코너 카메라 뱅크 롤 & 서스펜션 주행감] 🏎️💨 코너를 돌 때 화면과 지평선이 코너 안쪽으로 기울어지는 3D 카메라 롤링, 고저차 피칭, 연석 진동, 고속 배기 백파이어 불꽃 및 타이어 노면 먼지 이펙트 탑재!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 11,
        "versionName": "1.5.5",
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
                "latest_version": "1.5.5",
                "version_code": 11,
                "force_update": False,
                "release_notes": "장애물(빨간 위험 경고 링 & '!' 배지)과 아이템(시안·황금 빛기둥 & '?' 큐브) 완벽 시각 구분, 8대 코스별 대형 랜드마크·비행선·열기구 다층 배경, 코너 3D 카메라 뱅크 롤링 및 역동적 주행 연출 강화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.5 (build 11), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
