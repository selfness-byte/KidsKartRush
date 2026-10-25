#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.6.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.6.0.apk"
    notes = (
        "• [스킬 기반 드리프트 & 주행 물리 전면 개선] 진입 각도·유지 시간(GOOD/PERFECT/OVER)·해제 타이밍에 따라 탈출 부스트와 감속/라인 밀림이 갈리는 손맛 구현, 가드레일 비점착 탄성 리바운드 적용!\n"
        "• [대표 코스 '선셋 캐니언 에어로 서킷' 3랩 & 분기 지름길 완성] 직선 슬립스트림 추월 구간, 연속 S자 코너, 고저차 능선 분기(안전 본선 vs 위험 고속 협곡 데크 지름길), 180도 헤어핀 구간 탑재!\n"
        "• [경쟁형 AI 5대 & 핵심 전술 아이템 3종(터보 셀·쇼크 볼트·에너지 실드)] 고무줄 바인딩 제거, 공격형/안정형 AI 라인 선택 및 실수·회복, 후방 공격 경보(1.3초)와 실드 카운터 부스트/드리프트 회피 및 연속 피격 방지(2.5초 면역) 완성!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 15,
        "versionName": "1.6.0",
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
                "latest_version": "1.6.0",
                "version_code": 15,
                "force_update": False,
                "release_notes": "스킬 드리프트 물리(진입각·유지시간·해제타이밍 차등 보상), 대표 코스 '선셋 캐니언 에어로 서킷' 3랩 & 협곡 데크 지름길, 경쟁형 AI 5대(공격형/안정형), 핵심 전술 아이템 3종(터보 셀·쇼크 볼트·에너지 실드) 및 후방 경보·방어 카운터 완성.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.6.0 (build 15), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
