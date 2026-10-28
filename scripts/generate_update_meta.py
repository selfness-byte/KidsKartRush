#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-2.0.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-2.0.0.apk"
    notes = (
        "• [v2.0.0 익사이팅 팩: 훨씬 짜릿하고 신나게!] ① 연달아 격추하면 DOUBLE·TRIPLE·MEGA·ULTRA·MONSTER KILL 대형 콜 & 상승 사운드! ② 적이 터진 자리에 3D 화염구·충격파·파편 대폭발 + 화면 흔들림! ③ 보스 등장 시 ⚠WARNING⚠ 경고 띠 & 슬로모션, 보스 격파 시 연쇄 대폭발 + BOSS CLEAR!! 시네마틱! ④ 총알이 스칠 듯 피하면 😱NEAR MISS 보너스! ⑤ ⭐점수 & 콤보 배율(x2~x5) · 스테이지 클리어 보너스 · S/A/B/C 등급 & 최고 기록(NEW RECORD!) 도전! ⑥ FEVER가 특별한 순간에만 터지도록 밸런스 조정(8콤보 · 재충전 시간). ⑦ 탄환 식별 그래픽 개선: 🔵파랑=내 총알 · 🟢초록=동료 총알 · 🔴빨강 가시탄+검정 테두리+⊕도착 표적=적 총알로 어떤 배경에서도 한눈에 구분!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 28,
        "versionName": "2.0.0",
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
                "latest_version": "2.0.0",
                "version_code": 28,
                "force_update": False,
                "release_notes": "익사이팅 팩: 연속 처치 콜, 3D 대폭발·화면 흔들림, 보스 WARNING·슬로모션·BOSS CLEAR 연출, 니어미스 보너스, 점수·콤보 배율·S등급·최고기록 추가.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v2.0.0 (build 28), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
