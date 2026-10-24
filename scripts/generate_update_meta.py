#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.5.4.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.5.4.apk"
    notes = (
        "• [부스터 남발 방지 & 코너 리스크·오프로드 페널티 강화] 🚀 직선 자동 충전을 제거해 코너 드리프트·코인으로만 N2O를 모으도록 개선! 드리프트 없이 급코너에서 부스터를 켜면 원심력으로 코스 밖 오프로드/가드레일에 밀려 속도가 급감하고 부스터가 즉시 해제됩니다.\n"
        "• [슈퍼마리오 카트 명작 8대 코스 & 전용 기믹 완벽 반영] 🍄 마리오 서킷(토관·오일슬릭), 도넛 평원·초코섬(진흙 늪), 엉금엉금 비치(횡이동 꽃게), 바닐라 아이스 레이크(얼음 블록·빙판), 요시 밸리(구르는 거대 알), 피치 로얄 가든(미로 화단), 쿠파 성(내려찍는 쿵쿵이 바위), 무지개 로드(우주 쿵쿵이·무가드레일) 탑재!\n"
        "• [라이벌 AI 레이싱 경쟁력 대폭 강화] 🏎️ 결승선 앞 라이벌 감속 핸디캡을 폐지하고 코너 탈출 미니터보와 추격 부스터를 구사하도록 개편하여 정교한 드리프트와 코스 공략이 필수!"
    )

    update_payload = {
        "appName": "키즈 카트 러쉬! (Kids Kart Rush+)",
        "packageId": "com.mj.kidskart",
        "versionCode": 10,
        "versionName": "1.5.4",
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
                "latest_version": "1.5.4",
                "version_code": 10,
                "force_update": False,
                "release_notes": "드리프트 전용 부스터 충전·코너 부스터 오프로드 이탈 페널티로 부스터 남발 방지, 슈퍼마리오 카트 8대 코스 및 전용 기믹(쿵쿵이·거대 요시알·꽃게·얼음블록·진흙늪) 탑재, 라이벌 AI 코너 미니터보 경쟁력 강화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.5.4 (build 10), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
