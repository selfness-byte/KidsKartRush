#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.4.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.4.0.apk"
    notes = (
        "• [사운드] 🔊 속도가 빨라질수록 엔진음(V8 배기음·서브베이스·하모닉 오버드라이브·공명 필터)이 웅장하고 강력하게 증폭되도록 업그레이드!\n"
        "• [UI/UX] ✨ 주행 화면의 복잡한 글자들을 모두 없애고 직관적인 아기자기 아이콘만으로 깔끔하게 플레이하도록 개선\n"
        "• [아이템] 🎁 선물상자 리본 아이템 큐브, 웃는 바나나 요정, 천사 날개 등껍질, 스마일 별 코인, 하늘 고래 로켓 변신, 카트 옆 버블 아이템 프리뷰 등 아기자기한 3D 그래픽 적용\n"
        "• [AI 주행] 🏎️ 다른 차량들이 코너 라인을 따라 자연스럽게 조향·드리프트·추월하며 앞뒤로 실감 나게 경쟁하도록 물리 주행 개선\n"
        "• [8개 코스] 🗺️ 마리오 버섯 왕국, 슈가 캔디 랜드, 돌핀 비치 아일랜드, 펭귄 아이스 밸리, 요시 공룡 정글, 벚꽃 스프링 가든, 쿠파 용암 캐슬, 레인보우 스타 로드 총 8개 테마 코스로 대폭 확장!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 5,
        "versionName": "1.4.0",
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
                "latest_version": "1.4.0",
                "version_code": 5,
                "force_update": False,
                "release_notes": "가속할수록 강해지는 웅장한 V8 엔진 사운드, 주행 화면 글자 제거(클린 아이콘 HUD), 아기자기한 3D 아이템 그래픽, 자연스러운 라이벌 AI 코너링/추월 주행, 8종 테마 코스 확장.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.4.0 (build 5), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
