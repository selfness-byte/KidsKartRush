#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-2.0.1.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://inanimals-1977.web.app/kidskart/KidsKartRush-2.0.1.apk"
    notes = (
        "• [v2.0.1 자동업데이트 직통 CDN 개선 + 익사이팅 팩!] ① GitHub 리다이렉트 병목을 제거하고 Firebase CDN 직통 APK 배포 및 와이파이 재연결 자동 재시도·로비 자동 감지 적용! ② 연달아 격추하면 DOUBLE·TRIPLE·MEGA·ULTRA·MONSTER KILL 대형 콜 & 상승 사운드! ③ 적이 터진 자리에 3D 화염구·충격파·파편 대폭발 + 화면 흔들림! ④ 보스 등장 시 ⚠WARNING⚠ 경고 띠 & 슬로모션, 보스 격파 시 연쇄 대폭발 + BOSS CLEAR!! 시네마틱! ⑤ 총알이 스칠 듯 피하면 😱NEAR MISS 보너스! ⑥ ⭐점수 & 콤보 배율(x2~x5) · 스테이지 클리어 보너스 · S/A/B/C 등급 & 최고 기록(NEW RECORD!) 도전! ⑦ 탄환 식별 그래픽 개선: 🔵파랑=내 총알 · 🟢초록=동료 총알 · 🔴빨강 가시탄+검정 테두리+⊕도착 표적=적 총알!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 29,
        "versionName": "2.0.1",
        "apkUrl": apk_url,
        "sha256": sha256,
        "sizeBytes": size_bytes,
        "updatedAt": "2026-10-29",
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
                "latest_version": "2.0.1",
                "version_code": 29,
                "force_update": False,
                "release_notes": "자동업데이트 직통 CDN 호스팅 개선 + 익사이팅 팩(연속 처치 콜, 3D 대폭발·화면 흔들림, 보스 WARNING·슬로모션·BOSS CLEAR 연출, 니어미스 보너스, 점수·S등급·탄환 색 구분).",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v2.0.1 (build 29), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
