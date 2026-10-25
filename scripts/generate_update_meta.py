#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.2.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.2.apk"
    notes = (
        "• [캐릭터 나오는 모든 프레임에 얼굴 100% 정밀 맞춤] ① 로비 중앙 캐릭터 프리뷰 프레임(#previewCanvas 360x240)에서 얼굴이 상단에 잘리지 않고 프레임 정중앙에 들어오도록 조정, ② 카트 위 캐릭터 헤드/헬멧 원형 프레임(frameR=40)과 귀·리본·공룡뿔 장식에 맞춰 얼굴이 프레임 안에 빈틈없이 들어가도록 클리핑 정렬, ③ 로비 캐릭터 카드(.racer-face-wrap) 및 사진 스튜디오(.photo-slot-avatar) 원형 프레임에 기본 얼굴과 업로드 사진(피부톤·얼굴 중심 자동 검출 및 중복 크롭 방지)이 1:1로 딱 맞게 정렬!\n"
        "• [드리프트 시 실제 차 타이어 미끄러짐(촥~/스르륵~) 마찰음 적용] 시끄러운 전자 오실레이터음을 제거하고 실제 타이어가 아스팔트 노면에 쓸리는 물리 마찰음 적용!\n"
        "• [상대편 선행 출발 & 전방 총격전 시스템] 앞서 달리는 상대들이 전방에서 총을 쏘고, 내 카트도 프론트 트윈 개틀링건 상시 3점사 및 5종 중화기로 맞대응!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 20,
        "versionName": "1.9.2",
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
                "latest_version": "1.9.2",
                "version_code": 20,
                "force_update": False,
                "release_notes": "캐릭터 나오는 모든 프레임(로비 프리뷰·카트 헤드 프레임·캐릭터 선택 카드·사진 스튜디오)에 얼굴이 100% 딱 맞게 정렬되도록 개선.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.2 (build 20), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
