#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.8.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.8.apk"
    notes = (
        "• [1인 파트너 선택형 지원 시스템 & 사운드 완벽 복구!] ① 동료 레이서가 한꺼번에 몰려오거나 보급 캡슐에서 자동 소환되지 않고, 우측 패널에서 플레이어가 선택한 단 1명의 파트너만 나와서 도와주도록 개선(다시 누르면 즉시 복귀하여 혼자 주행!), ② 태블릿·스마트폰 스피커 및 웹뷰에서 소리가 안 나던 문제 완벽 해결(마스터 게인 2.35x 증폭 + 다이내믹 컴프레서, 터치 즉시 오디오 언락, 88~340Hz 가청 대역 V8 배기음 & 신나는 레이싱 신스 BGM 루프, 안드로이드 미디어 볼륨 스트림 연동)!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 26,
        "versionName": "1.9.8",
        "apkUrl": apk_url,
        "sha256": sha256,
        "sizeBytes": size_bytes,
        "updatedAt": "2026-10-26",
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
                "latest_version": "1.9.8",
                "version_code": 26,
                "force_update": False,
                "release_notes": "우측에서 선택한 단 1명의 동료만 출격·복귀하는 선택형 지원 시스템 적용 및 엔진음·사격음·BGM 사운드 출력 완벽 복구.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.8 (build 26), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
