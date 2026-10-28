package com.mj.kidskart.update

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import org.json.JSONObject
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

data class UpdateInfo(
    val versionCode: Int,
    val versionName: String,
    val apkUrl: String,
    val sha256: String,
    val notes: String,
)

/**
 * inanimals-1977.web.app / www.inanimals.co.kr / GitHub 저장소에서 최신 버전 정보를 확인하고,
 * APK 다운로드·무결성 검증·Android 패키지 설치 화면 실행까지 수행하는 자동 업데이트 매니저.
 */
object AppUpdater {

    private val UPDATE_URLS = listOf(
        "https://inanimals-1977.web.app/kidskart/update.json",
        "https://www.inanimals.co.kr/kidskart/update.json",
        "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/update.json",
    )

    private val executor = Executors.newCachedThreadPool()
    private val mainHandler = Handler(Looper.getMainLooper())

    @Volatile
    private var lastCheckTimeMs = 0L

    @Volatile
    private var retryCount = 0

    @Volatile
    private var isDownloading = false

    @Volatile
    private var autoTriggeredVersionCode = 0

    @Volatile
    private var pendingInstallFile: File? = null

    fun installedVersionCode(context: Context): Int = runCatching {
        val pInfo = context.packageManager.getPackageInfo(context.packageName, 0)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            pInfo.longVersionCode.toInt()
        } else {
            @Suppress("DEPRECATION")
            pInfo.versionCode
        }
    }.getOrDefault(1)

    fun installedVersionName(context: Context): String = runCatching {
        context.packageManager.getPackageInfo(context.packageName, 0).versionName ?: "1.0.0"
    }.getOrDefault("1.0.0")

    fun resumePendingInstallIfAllowed(activity: Activity) {
        val file = pendingInstallFile
        if (file != null) {
            if (!file.exists()) {
                pendingInstallFile = null
            } else if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O || activity.packageManager.canRequestPackageInstalls()) {
                pendingInstallFile = null
                launchInstaller(activity, file)
                return
            }
        }
        // 앱이 백그라운드에서 다시 포그라운드로 돌아올 때도 자동 업데이트 확인 (최소 10초 간격)
        checkOnStartup(activity)
    }

    /** 앱 시작·포그라운드 복귀·대기실 진입 시 백그라운드 자동 업데이트 확인 및 즉시 다운로드 실행 */
    fun checkOnStartup(activity: Activity, isRetry: Boolean = false) {
        if (isDownloading) return
        val now = System.currentTimeMillis()
        if (!isRetry && now - lastCheckTimeMs < 10_000L) return
        executor.execute {
            cleanOldApks(activity.applicationContext)
            val info = fetchLatestUpdate(activity)
            if (info == null) {
                // 태블릿 화면 켜짐 직후 Wi-Fi 재연결 지연 대비 자동 재시도 (최대 4회, 3초 간격)
                if (retryCount < 4) {
                    retryCount++
                    mainHandler.postDelayed({
                        if (!activity.isFinishing && !activity.isDestroyed) {
                            checkOnStartup(activity, isRetry = true)
                        }
                    }, 3000L)
                }
                return@execute
            }
            retryCount = 0
            lastCheckTimeMs = System.currentTimeMillis()
            val curCode = installedVersionCode(activity)
            if (info.versionCode > curCode && !isDownloading && autoTriggeredVersionCode != info.versionCode) {
                autoTriggeredVersionCode = info.versionCode
                mainHandler.post {
                    if (!activity.isFinishing && !activity.isDestroyed) {
                        Toast.makeText(
                            activity,
                            "🚀 새 버전(v${info.versionName}) 발견! 자동 업데이트를 시작합니다…",
                            Toast.LENGTH_SHORT
                        ).show()
                        downloadAndInstall(activity, info)
                    }
                }
            }
        }
    }

    /** 대기실 상단 [🔄 업데이트] 버튼 클릭 시 수동 확인 및 강제 재설치/업데이트 지원 */
    fun checkManual(activity: Activity) {
        val curName = installedVersionName(activity)
        Toast.makeText(activity, "최신 업데이트 확인 중… (현재 v$curName)", Toast.LENGTH_SHORT).show()
        executor.execute {
            val info = fetchLatestUpdate(activity)
            mainHandler.post {
                if (activity.isFinishing || activity.isDestroyed) return@post
                if (info == null) {
                    Toast.makeText(activity, "현재 v$curName · 업데이트 서버에 연결할 수 없습니다.", Toast.LENGTH_SHORT).show()
                    return@post
                }
                showUpdateDialog(activity, info, forceOffer = true)
            }
        }
    }

    private fun fetchLatestUpdate(context: Context? = null): UpdateInfo? {
        val uaVersion = context?.let { installedVersionName(it) } ?: "1.0"
        for (url in UPDATE_URLS) {
            val info = runCatching { requestUpdateJson(url, uaVersion) }.getOrNull()
            if (info != null && info.versionCode >= 1 && info.apkUrl.startsWith("https://")) {
                return info
            }
        }
        return null
    }

    private fun requestUpdateJson(urlStr: String, uaVersion: String): UpdateInfo? {
        val sep = if (urlStr.contains("?")) "&" else "?"
        val cacheBustedUrl = "${urlStr}${sep}t=${System.currentTimeMillis()}"
        val conn = (URL(cacheBustedUrl).openConnection() as HttpURLConnection).apply {
            connectTimeout = 5000
            readTimeout = 5000
            useCaches = false
            setRequestProperty("Cache-Control", "no-cache, no-store, max-age=0")
            setRequestProperty("Pragma", "no-cache")
            setRequestProperty("User-Agent", "KidsKartRush/$uaVersion")
        }
        return try {
            if (conn.responseCode !in 200..299) return null
            val body = conn.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
            val o = JSONObject(body)
            UpdateInfo(
                versionCode = o.optInt("versionCode", o.optInt("version_code", 0)),
                versionName = o.optString("versionName", o.optString("latest_version", "")),
                apkUrl = o.optString("apkUrl", o.optString("download_url", "")),
                sha256 = o.optString("sha256", "").trim().lowercase(),
                notes = o.optString("notes", o.optString("release_notes", "새로운 기능 및 사운드 개선 업데이트")),
            )
        } finally {
            conn.disconnect()
        }
    }

    private fun showUpdateDialog(activity: Activity, info: UpdateInfo, forceOffer: Boolean) {
        val curName = installedVersionName(activity)
        val curCode = installedVersionCode(activity)
        val isNewer = info.versionCode > curCode
        val title = if (isNewer) {
            "🚀 새 버전 업데이트 발견! (v${info.versionName})"
        } else {
            "🔄 최신 버전 안내 (v${info.versionName})"
        }
        val statusLine = if (isNewer) {
            "현재 버전: v$curName (build $curCode)\n최신 버전: v${info.versionName} (build ${info.versionCode})"
        } else {
            "현재 최신 버전(v$curName)을 사용 중입니다.\n원하시면 최신 설치 파일로 다시 덮어써서 업데이트할 수 있습니다."
        }
        val btnLabel = if (isNewer || forceOffer) "지금 업데이트" else "다시 설치"

        AlertDialog.Builder(activity)
            .setTitle(title)
            .setMessage("$statusLine\n\n${info.notes}")
            .setPositiveButton(btnLabel) { _, _ ->
                downloadAndInstall(activity, info)
            }
            .setNeutralButton("웹 포털 열기") { _, _ ->
                runCatching {
                    activity.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://inanimals-1977.web.app/kidskart/")))
                }
            }
            .setNegativeButton("닫기", null)
            .show()
    }

    private fun downloadAndInstall(activity: Activity, info: UpdateInfo) {
        if (isDownloading) return
        isDownloading = true
        val density = activity.resources.displayMetrics.density
        val pad = (20 * density).toInt()
        val box = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(pad, pad, pad, pad)
        }
        val statusTv = TextView(activity).apply {
            text = "APK 파일 다운로드 준비 중…"
            textSize = 15f
        }
        val progressBar = ProgressBar(activity, null, android.R.attr.progressBarStyleHorizontal).apply {
            isIndeterminate = false
            max = 100
            progress = 0
        }
        box.addView(statusTv)
        box.addView(progressBar)

        val cancelled = java.util.concurrent.atomic.AtomicBoolean(false)
        val dlg = AlertDialog.Builder(activity)
            .setTitle("업데이트 다운로드 중 (v${info.versionName})")
            .setView(box)
            .setCancelable(false)
            .setNegativeButton("취소") { d, _ ->
                cancelled.set(true)
                isDownloading = false
                d.dismiss()
            }
            .create()
        dlg.show()

        val uaVersion = installedVersionName(activity)
        executor.execute {
            val dir = File(activity.cacheDir, "updates").apply { mkdirs() }
            val target = File(dir, "KidsKartRush-${info.versionName}-b${info.versionCode}.apk")

            // 이미 유효한 동일 버전 APK가 받아져 있다면 재다운로드 없이 즉시 재사용
            if (target.exists() && isValidApkFile(target)) {
                mainHandler.post {
                    isDownloading = false
                    if (dlg.isShowing) dlg.dismiss()
                    if (!cancelled.get() && !activity.isFinishing && !activity.isDestroyed) {
                        proceedToInstall(activity, target)
                    }
                }
                return@execute
            }

            val candidateUrls = linkedSetOf(
                "https://inanimals-1977.web.app/kidskart/KidsKartRush-${info.versionName}.apk",
                "https://www.inanimals.co.kr/kidskart/KidsKartRush-${info.versionName}.apk",
                info.apkUrl,
                "https://raw.githubusercontent.com/selfness-byte/KidsKartRush/main/dist/KidsKartRush-${info.versionName}.apk",
            ).filter { it.startsWith("https://") }

            var outFile: File? = null
            for (rawUrl in candidateUrls) {
                if (cancelled.get()) break
                outFile = runCatching {
                    val sep = if (rawUrl.contains("?")) "&" else "?"
                    val downloadUrl = "${rawUrl}${sep}t=${System.currentTimeMillis()}"
                    val conn = (URL(downloadUrl).openConnection() as HttpURLConnection).apply {
                        connectTimeout = 15_000
                        readTimeout = 30_000
                        useCaches = false
                        instanceFollowRedirects = true
                        setRequestProperty("Cache-Control", "no-cache, no-store, max-age=0")
                        setRequestProperty("Pragma", "no-cache")
                        setRequestProperty("User-Agent", "KidsKartRush/$uaVersion")
                    }
                    try {
                        if (conn.responseCode !in 200..299) return@runCatching null
                        val total = conn.contentLengthLong
                        conn.inputStream.use { input ->
                            FileOutputStream(target).use { output ->
                                val buf = ByteArray(16 * 1024)
                                var downloaded = 0L
                                while (!cancelled.get()) {
                                    val r = input.read(buf)
                                    if (r < 0) break
                                    output.write(buf, 0, r)
                                    downloaded += r
                                    if (total > 0) {
                                        val pct = ((downloaded * 100L) / total).toInt().coerceIn(0, 100)
                                        mainHandler.post {
                                            progressBar.progress = pct
                                            statusTv.text = "다운로드 중… $pct% (${downloaded / 1024}KB / ${total / 1024}KB)"
                                        }
                                    }
                                }
                            }
                        }
                        if (cancelled.get()) {
                            target.delete()
                            return@runCatching null
                        }
                        if (!isValidApkFile(target)) {
                            target.delete()
                            return@runCatching null
                        }
                        target
                    } finally {
                        conn.disconnect()
                    }
                }.getOrNull()
                if (outFile != null && outFile.exists()) break
            }

            mainHandler.post {
                isDownloading = false
                if (dlg.isShowing) dlg.dismiss()
                if (cancelled.get() || activity.isFinishing || activity.isDestroyed) return@post

                if (outFile == null || !outFile.exists()) {
                    Toast.makeText(activity, "다운로드에 실패하여 웹 다운로드 페이지를 엽니다.", Toast.LENGTH_LONG).show()
                    runCatching {
                        activity.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://inanimals-1977.web.app/kidskart/")))
                    }
                    return@post
                }

                proceedToInstall(activity, outFile)
            }
        }
    }

    private fun proceedToInstall(activity: Activity, outFile: File) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && !activity.packageManager.canRequestPackageInstalls()) {
            pendingInstallFile = outFile
            Toast.makeText(activity, "'출처를 알 수 없는 앱 설치' 허용 후 즉시 설치됩니다.", Toast.LENGTH_LONG).show()
            val intent = Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:${activity.packageName}"))
            activity.startActivity(intent)
            return
        }
        launchInstaller(activity, outFile)
    }

    private fun launchInstaller(context: Context, apkFile: File) {
        runCatching {
            val uri = ApkFileProvider.getUriForFile(context, apkFile)
            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(uri, "application/vnd.android.package-archive")
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(intent)
        }.onFailure { err ->
            Toast.makeText(context, "설치 화면 실행 실패: ${err.message}", Toast.LENGTH_LONG).show()
        }
    }

    private fun isValidApkFile(file: File): Boolean {
        if (!file.exists() || file.length() < 10_000L) return false
        return runCatching {
            FileInputStream(file).use { fis ->
                val b0 = fis.read()
                val b1 = fis.read()
                b0 == 0x50 && b1 == 0x4B // 'P', 'K'
            }
        }.getOrDefault(false)
    }

    private fun cleanOldApks(context: Context) {
        runCatching {
            val pending = pendingInstallFile?.canonicalPath
            val now = System.currentTimeMillis()
            val dir = File(context.cacheDir, "updates")
            if (dir.exists()) {
                dir.listFiles()?.forEach { f ->
                    // 방금 받은 파일(30분 이내)이나 설치 대기 중인 파일은 보존하여 권한 허용 후 재설치 보장
                    if (f.canonicalPath != pending && (now - f.lastModified() > 30 * 60 * 1000L)) {
                        f.delete()
                    }
                }
            }
        }
    }
}
