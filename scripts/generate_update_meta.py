#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.9.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.9.apk"
    notes = (
        "• [3-STAGE 롱 캠페인 · 적 전투헬기(🚁) & 기갑 탱크(🚜) 출격 · 중간보스 빈도 대폭 완화!] ① 스테이지 주행 거리를 33% 확장(720 세그먼트)하고 STAGE 1(🌅선셋 데저트 캐니언) → STAGE 2(❄️오로라 설원 기갑요새) → STAGE 3(🌋크림슨 화산 드래곤 성채)마다 하늘·지형·도로 분위기가 완전히 전환되도록 업그레이드! ② 4엽 메인 로터가 회전하며 로켓포드를 쏘는 3D 적 전투헬기(🚁)와 무한궤도·대구경 주포를 갖춘 적 기갑 탱크(🚜) 등 스테이지별 전용 적 군단 편성! ③ 중간보스가 너무 자주 나오지 않도록 스테이지당 딱 1회(Stage 1 🤖스콜피온 -> Stage 2 🛸아크틱 건십 -> Stage 3 🐉거대 화염 드래곤, 총 3회)만 등장하고 처치 후에는 전방 적 헬기·탱크 부대만 출현하도록 개선!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 27,
        "versionName": "1.9.9",
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
                "latest_version": "1.9.9",
                "version_code": 27,
                "force_update": False,
                "release_notes": "3-STAGE 롱 캠페인(사막 협곡 → 설원 기갑요새 → 화산 드래곤 성채) 분위기 전환, 적 전투헬기(🚁)·기갑 탱크(🚜) 추가, 스테이지당 보스 1회 출현으로 중간보스 빈도 대폭 완화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.9 (build 27), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
