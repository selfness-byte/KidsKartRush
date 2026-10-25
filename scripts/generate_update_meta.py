#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.1.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.1.apk"
    notes = (
        "• [드리프트 시 실제 자동차 타이어 미끄러짐(촥~/스르륵~) 마찰음으로 전면 개선] 귀가 피로한 고주파 전자 오실레이터음을 완전히 제거하고, 핑크 노이즈·트레드 그레인 모듈레이션·680Hz 타이어 바디 공명·1,280Hz 로우패스 필터를 결합해 실제 차가 아스팔트 노면에 묵직하게 쓸리며 미끄러지는 타이어 슬립 사운드로 개선!\n"
        "• [상대편 선행 출발 & 하드코어 AI 난이도 상향] 상대 카트 5대가 출발부터 플레이어 앞으로 치고 나가며(초기 6위 출발), 주행 페이스(1.125~1.185)와 추월 가속(1.16~1.24 + N2O 부스트)으로 끝까지 치열한 추격전 진행!\n"
        "• [전방 총격전 시스템 (앞에서 상대가 총을 쏘고 & 내 카트 기본 기관총 + 중화기 5종 사격)] 앞서 달리는 상대들이 전방에서 기관총탄·레이저탄(조준 경고선 표시)을 발사하며, 내 카트도 프론트 트윈 개틀링건으로 상시 3점사 사격 및 5종 중화기로 맞대응!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 19,
        "versionName": "1.9.1",
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
                "latest_version": "1.9.1",
                "version_code": 19,
                "force_update": False,
                "release_notes": "드리프트 시 시끄러운 전자음 제거 및 실제 차가 아스팔트 노면에 미끄러지는 타이어 마찰음(tireSlideBuffer) 적용, 상대편 전방 선행 및 전방 총격전 시스템 완성.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.1 (build 19), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
