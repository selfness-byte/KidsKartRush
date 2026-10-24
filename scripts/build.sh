#!/bin/zsh
# 키즈 카트 러쉬 APK 빌드 및 태블릿 설치 스크립트 (외장하드 M 전용)
set -e
if [ ! -d /Volumes/MDev ]; then
  hdiutil attach /Volumes/M/DevTools/MDev.sparsebundle
fi
source /Volumes/M/DevTools/env.sh
PROJECT=/Volumes/M/KidsKartRush_20261024
cd "$PROJECT"
dot_clean -m "$PROJECT" 2>/dev/null || true
gradle --offline --project-cache-dir /Volumes/MDev/project-cache/KidsKartRush :app:assembleDebug --console=plain
mkdir -p "$PROJECT/dist"
cp "$NRM_BUILD_ROOT/KidsKartRush/app/outputs/apk/debug/app-debug.apk" "$PROJECT/dist/KidsKartRush-debug.apk"
cp "$NRM_BUILD_ROOT/KidsKartRush/app/outputs/apk/debug/app-debug.apk" "$PROJECT/dist/KidsKartRush-1.5.8.apk"
python3 "$PROJECT/scripts/generate_update_meta.py"
echo "APK: $PROJECT/dist/KidsKartRush-1.5.8.apk"
if [ "$1" = "--install" ]; then
  adb -d install -r "$PROJECT/dist/KidsKartRush-1.5.8.apk"
  adb -d shell am start -n com.mj.kidskart/.MainActivity
fi
