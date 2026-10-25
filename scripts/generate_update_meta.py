#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.4.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.4.apk"
    notes = (
        "• [전방 적 군단(3종) & 3단계 거대 보스전(Giant Boss Battle) 시스템 신설!] ① 트랙 위를 편대 비행·주행하며 플레이어를 공격하는 3종 적 기체(👾스카이 전투 드론 · 🏍️아머드 바이커 · 🛡️헤비 메카 탱크) 상시 출현 및 격추 시 부스트/중화기 보상, ② 전방 도로를 장악하며 2연장 플라즈마 캐논과 3갈래 보스 레이저를 쏘는 3단계 거대 보스(Lv.1 🤖아이언 스콜피온 메카 -> Lv.2 🛸네온 디스트로이어 건십 -> Lv.3 🐉메카 드래곤 엠페러) 및 상단 실시간 보스 HP 게이지 바 추가, ③ 보스 격파 시 연쇄 대폭발과 함께 무적 슈퍼 풀부스트 + N2O 완충 + 중화기 보상 지급!\n"
        "• [총알 쏘는 타격감 & 3-Layer 실감 탄도 사운드] 총구에서 적/보스까지 뻗어나가는 3D 예광탄 궤적 광선, 황동 탄피 배출, 연사 손맛, 명중 히트마커 및 묵직한 총성/장갑 타격음 적용!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 22,
        "versionName": "1.9.4",
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
                "latest_version": "1.9.4",
                "version_code": 22,
                "force_update": False,
                "release_notes": "전방 적 군단(드론·바이커·메카탱크) 및 3단계 거대 보스전(아이언 스콜피온·네온 디스트로이어·메카 드래곤) 추가.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.4 (build 22), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
