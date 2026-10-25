#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

PROJECT_DIR = Path("/Volumes/M/KidsKartRush_20261024")
APK_PATH = PROJECT_DIR / "dist" / "KidsKartRush-1.9.3.apk"

def main():
    if not APK_PATH.exists():
        raise FileNotFoundError(f"APK not found: {APK_PATH}")

    data = APK_PATH.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    size_bytes = len(data)

    apk_url = "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-1.9.3.apk"
    notes = (
        "• [총알 쏘는 타격감 & 실감 탄도 사운드 대폭 업그레이드] ① 3-Layer 실감 총성 합성(총구 폭발 저음 펀치 + 화약 파열 크랙 + 노리쇠/황동 탄피 금속 클락) 및 적 카트 장갑 명중 타격음('챙-퍽!') 추가, ② 사격 버튼(🔫) 터치 시 즉각 3점사 + 버튼을 누르고 있으면 트윈 개틀링 기관총이 좌·우 번갈아 고속 자동 연사(Hold-to-Fire), ③ 카트 총구에서 전방 도로 표적까지 뻗어나가는 초고속 3D 예광탄 궤적 광선(Tracer Beam) + 사방으로 튕기는 황동 탄피(Shell Casing) + 총열 반동(Recoil) + 명중 크로스헤어(🎯 HIT!) 연출 적용!\n"
        "• [캐릭터 나오는 모든 프레임에 얼굴 100% 정밀 맞춤] 로비 프리뷰·카트 위 캐릭터 헤드 원형 프레임·로비 카드·사진 스튜디오 프레임에 얼굴이 빈틈없이 정렬!\n"
        "• [드리프트 시 실제 차 타이어 미끄러짐(촥~/스르륵~) 마찰음 적용] 아스팔트 노면과 타이어 고무가 쓸리는 리얼 물리 마찰음 적용!"
    )

    update_payload = {
        "appName": "에어로 카트 GP: 선셋 캐니언 에디션",
        "packageId": "com.mj.kidskart",
        "versionCode": 21,
        "versionName": "1.9.3",
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
                "latest_version": "1.9.3",
                "version_code": 21,
                "force_update": False,
                "release_notes": "총알 쏘는 타격감(3D 예광탄 궤적 광선·황동 탄피 배출·연사 손맛·명중 히트마커) 및 3-Layer 실감 총성/장갑 타격음 대폭 강화.",
                "download_url": apk_url,
                "sha256": sha256,
                "size_bytes": size_bytes,
            }
            vf.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Updated metadata: v1.9.3 (build 21), sha256={sha256}, size={size_bytes}")

if __name__ == "__main__":
    main()
