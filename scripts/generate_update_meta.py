#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.7.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.7.apk"
    notes = (
        "• [초장거리 후퇴(1130m) ↔ 초근접 급강하(120m) 적 기체 기동 & 4대 아케이드 재미 요소 대폭 추가!] ① 적들이 지평선 근처 초장거리(960~1150m)까지 훨씬 멀리 떨어졌다가 제트 부스터 불꽃을 뿜으며 플레이어 코앞(115~145m)으로 급강하 돌진하는 다이내믹 왕복 기동 적용, ② 5연속 격추 시 5갈래 스타버스트 탄막이 폭발하는 🔥연쇄 콤보 & ⚡FEVER OVERDRIVE 각성 시스템, ③ 적 격추 시 도로 위에 떨어지는 🎁3D 홀로그램 보급 캡슐(⚡하이퍼 발칸 오버차지 · 🧲코인 잭팟 · 🤝동료 긴급 호출), ④ 보스 몸체의 회전 과녁을 맞히면 2~3배 데미지가 터지는 🎯WEAK POINT 크리티컬 사격 및 🌈동료 5인 합체 레인보우 레이저 포격 탑재!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 25,
        "versionName": "1.9.7",
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
                "latest_version": "1.9.7",
                "version_code": 25,
                "force_update": False,
                "release_notes": "초장거리 후퇴-초근접 급강하 적 기동, 5콤보 FEVER OVERDRIVE 각성, 3D 보급 캡슐 드롭, 보스 약점 크리티컬 사격 및 동료 합체 레인보우 레이저 추가.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.7 (build 25), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
