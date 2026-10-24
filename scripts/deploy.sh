#!/bin/zsh
# GitHub 및 Firebase Hosting(inanimals-1977.web.app / www.inanimals.co.kr) 배포 스크립트
set -e

PROJECT=/Volumes/M/KidsKartRush_20261024
GH_BIN=/Volumes/M/Tools/gh_2.102.0_macOS_arm64/bin/gh
FIREBASE_BIN=/usr/local/bin/firebase

dot_clean -m "$PROJECT" /Volumes/M/firebase-app-update-server /Volumes/M/inanimals-corp-website 2>/dev/null || true

cd "$PROJECT"
"$GH_BIN" auth setup-git || true
if ! "$GH_BIN" repo view selfness-byte/KidsKartRush >/dev/null 2>&1; then
  git remote remove origin 2>/dev/null || true
  "$GH_BIN" repo create selfness-byte/KidsKartRush --public --source="$PROJECT" --remote=origin --push
else
  git remote add origin https://github.com/selfness-byte/KidsKartRush.git 2>/dev/null || true
  git push -u origin main
fi

echo "=== Deploying to inanimals-1977.web.app ==="
cd /Volumes/M/firebase-app-update-server
"$FIREBASE_BIN" deploy --only hosting

echo "=== Deploying to inanimals-corp-1977 (www.inanimals.co.kr) ==="
cd /Volumes/M/inanimals-corp-website
"$FIREBASE_BIN" deploy --only hosting

echo "=== Deployment Complete ==="
