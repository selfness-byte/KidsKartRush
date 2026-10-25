#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.6.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.6.apk"
    notes = (
        "• [우측 동료 레이서 클릭 지원 출격 & 원거리-근거리 파도타기 적군 & 거대 화염 용(🐉) 보스전 대개편!] ① 나머지 5명의 레이서를 화면 오른쪽 지원 버튼으로 클릭하면 즉시 트랙 위로 출격해 적과 보스를 함께 공격하며 도와주는 아군 윙맨(Ally Support) 시스템 탑재, ② 적 기체들이 현재의 전방 위치에서 멀리서 총을 쏘다가 가까워졌다가 다시 멀어지는 원거리-근거리 왕복 기동 적용, ③ 중간보스(🤖아이언 스콜피온)는 1회 처치 시 다시 나오지 않고 저 멀리서 작은 적들이 몰려오는 웨이브로 전환된 뒤 대망의 큰 보스전 거대 화염 용(🐉 드래곤 엠페러)이 강림하도록 구성!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 24,
        "versionName": "1.9.6",
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
                "latest_version": "1.9.6",
                "version_code": 24,
                "force_update": False,
                "release_notes": "우측 레이서 클릭 지원 출격, 원거리-근거리 파도타기 적 기체, 중간보스 1회 처치 후 작은 적 원거리 웨이브 및 거대 화염 용(드래곤) 보스전 적용.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.6 (build 24), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
