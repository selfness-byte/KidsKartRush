#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.1.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.1.0.apk"
    notes = (
        "• [신규] 🏎️ 5대의 라이벌 카트(다오·디지니·배찌·우니·마리드·모비)가 내 바로 앞에서 앞서 달리며 경쟁하고 부스터로 추월하는 스마트 페이스메이커 AI 탑재\n"
        "• [신규] 🔊 리얼 자동차 레이싱 효과음 합성 엔진(시동 크랭킹 & V6 배기 레브업, 1~5단 기어 변속 연동 실시간 연속 RPM 엔진음, 드리프트 타이어 스키드 마찰음, 터보 블로우오프 & 니트로 제트 화염 부스터음, 듀얼톤 자동차 클락션)\n"
        "• [신규] 🔄 앱 시작 시 자동 업데이트 확인 및 대기실 상단 [🔄 업데이트] 원클릭 다운로드·설치 지원\n"
        "• ⛑️ 어린이 맞춤 3중 터치 핸들(Steering Wheel) 컨트롤러 & 코너 자동 유도 도우미"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 2,
        "versionName": "1.1.0",
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
                "latest_version": "1.1.0",
                "version_code": 2,
                "force_update": False,
                "release_notes": "5대 라이벌 카트 전방 경쟁 주행, 리얼 자동차 엔진·기어변속·타이어 스키드·터보 부스터·듀얼톤 클락션 효과음, 앱 내 자동 업데이트 지원.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.1.0 (build 2), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
