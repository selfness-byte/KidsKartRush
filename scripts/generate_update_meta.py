#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.7.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.7.apk"
    notes = (
        "• [여성 음성(TTS) 100% 완전 제거] 🔇 네이티브 Android TTS 및 브라우저 음성 합성을 모두 제거하여, 여성 안내 음성 없이 중후한 V8 엔진 배기음·타이어 마찰음·부스터 제트 사운드에만 온전히 몰입할 수 있습니다!\n"
        "• [카트라이더(KartRider) 정통 드리프트 & 끌기 & 순간 부스터(순부) 완벽 구현] 🏎️💨 핸들을 깊게 꺾거나 휙 꺾으면 언제 어디서나 즉시 '끼이이익~!' 타이어 마찰음과 함께 차체가 대각선으로 깊게 꺾이며 인코스를 파고드는 카트라이더 드리프트가 발동됩니다!\n"
        "• [반대 방향 카운터 스티어링(드리프트 끊기) & 순부 점화] 드리프트로 N2O 게이지를 빠르게 채우고(최대 2개 부스터🔥 스택), 반대 방향 카운터 스티어링이나 핸들 복귀 시 카트라이더 시그니처 '순간 부스터(순부)'가 터집니다!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 13,
        "versionName": "1.5.7",
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
                "app_name": "키즈 카트 러쉬!",
                "latest_version": "1.5.7",
                "version_code": 13,
                "force_update": False,
                "release_notes": "여성 음성(TTS) 완전 제거, 카트라이더 정통 드리프트(깊은 사선 슬라이딩·끌기 N2O 충전·반대 방향 카운터 스티어링 드리프트 끊기·순간 부스터 점화) 완벽 구현.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.7 (build 13), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
