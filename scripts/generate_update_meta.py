#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.6.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.6.apk"
    notes = (
        "• [인공 경기장 트랙 대신 8대 대자연 모험 월드 표현] 🌍 회색 아스팔트·3차선 점선·흰색 실선·적백 연석·반사봉을 모두 걷어내고, 구불구불한 자연 지형(버섯 왕국 들판·스위트 디저트 동산·코랄 오션 해변 파도거품·오로라 빙하 설원·공룡 정글 사파리·로얄 벚꽃 동산·드래곤 화산 협곡·은하수 별빛 하늘길)으로 표현!\n"
        "• [경적 완전 제거 & 부스터🔥·아이템🎁 2버튼 메뉴 단순화] 핸들 중앙 경적(📯)과 우측 드리프트 버튼·상단 중복 슬롯을 모두 없애고, 오직 '아이템 던지는 버튼(🎁)'과 '부스터 아이콘 버튼(🔥)' 2개만 남겨 훨씬 깔끔하고 직관적인 조작 완성!\n"
        "• [핸들 조향 자동 코너 드리프트 & 미니터보] 별도 드리프트 버튼 없이도 코너에서 핸들을 꺾으면 자연스럽게 드리프트 슬라이딩하며 N2O 게이지 충전 및 코너 탈출 미니터보가 자동 발동됩니다!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 12,
        "versionName": "1.5.6",
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
                "latest_version": "1.5.6",
                "version_code": 12,
                "force_update": False,
                "release_notes": "인공 트랙 대신 8대 대자연 모험 월드(들판·해변 파도·설원·정글·화산·은하수) 지형 표현, 경적 완전 제거, 우측 메뉴를 부스터(🔥)와 아이템 던지기(🎁) 2버튼으로 단순화 및 핸들 자동 코너 드리프트 적용.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.6 (build 12), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
