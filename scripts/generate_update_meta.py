#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.2.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.2.apk"
    notes = (
        "• [짧고 강렬한 '슈웅~!' 슈퍼부스터] 🚀 슈퍼부스터 지속시간을 짧고 경쾌하게 단축하고, 누르는 순간 앞으로 튀어나가는 폭발적 초반 가속감 적용!\n"
        "• ['슈우웅~!' 제트 터보 효과음] 🔊 부스터 버튼을 누를 때 바람을 가르는 에어로다이나믹 스윕 + 트윈 터보 제트 휘슬 사운드('슈우웅~!')로 업그레이드\n"
        "• [하이퍼 워프 화면 속도감 연출] ⚡ 부스터 발동 시 3D 카메라 광각 FOV 워프(줌 아웃) + 3D 소닉 충격파 링 + 소실점 방사형 워프 라인 + 초음속 제트 불꽃 연출\n"
        "• [정통 3D 원근 & 얼굴 사진 스튜디오] 📸 정통 1/Z 3D 원근 트랙, 내 캐릭터 및 모든 라이벌 머리 사진 업로드, 1:1 직관적 핸들 조작 지원!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 8,
        "versionName": "1.5.2",
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
                "latest_version": "1.5.2",
                "version_code": 8,
                "force_update": False,
                "release_notes": "짧고 강렬한 슈퍼부스터 & 누를 때 '슈우웅~!' 제트 터보 사운드 + 3D 카메라 FOV 광각 워프·소닉 충격파 링 화면 속도감 극대화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.2 (build 8), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
