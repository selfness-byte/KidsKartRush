#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.0.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.0.apk"
    notes = (
        "• [얼굴 사진 커스텀] 📸 내 캐릭터는 물론 다른 레이서 5명의 머리에도 갤러리/카메라 얼굴 사진을 올리고 주행 중 생생하게 볼 수 있도록 지원!\n"
        "• [지면 밀착 & 흔들림 제거] 🏎️ 자동차가 붕 뜨거나 캐릭터가 흔들리던 현상을 완벽히 해결하여 아스팔트 노면에 묵직하고 매끄럽게 밀착 주행\n"
        "• [직관적 1:1 핸들 조작] 🛞 핸들 좌우 터치 방향 그대로 차가 즉각적이고 부드럽게 움직이도록 조향 물리 전면 개선\n"
        "• [아기자기한 아이템 비율] 🎁 시야를 가리던 트랙 아이템 크기를 약 48% 축소하여 아기자기하고 깔끔한 비율로 최적화\n"
        "• [하이스피드 & 8종 코스 노면] 🚀 주행 속도감 대폭 상향, 3차선 고속 점선·스피드 라인 및 8가지 코스별 고유 노면 패턴 적용!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 6,
        "versionName": "1.5.0",
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
                "latest_version": "1.5.0",
                "version_code": 6,
                "force_update": False,
                "release_notes": "내 캐릭터 및 모든 라이벌 레이서 머리 얼굴 사진 업로드 지원, 지면 밀착형 3D 카트 렌더링(붕 뜸·흔들림 완전 해결), 1:1 직관적 핸들 조작, 아기자기한 소형 아이템 비율, 하이스피드 속도감 및 8종 코스 노면 다양화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.0 (build 6), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
