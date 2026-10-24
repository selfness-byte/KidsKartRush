package com.mj.kidskart

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.speech.tts.TextToSpeech
import android.view.View
import android.view.WindowInsets
import android.view.WindowInsetsController
import android.view.WindowManager
import android.webkit.JavascriptInterface
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import com.mj.kidskart.update.AppUpdater
import java.util.Locale

class MainActivity : Activity(), TextToSpeech.OnInitListener, SensorEventListener {

    private lateinit var webView: WebView
    private var tts: TextToSpeech? = null
    private var ttsReady = false
    private var sensorManager: SensorManager? = null
    private var accelSensor: Sensor? = null
    private var fileUploadCallback: ValueCallback<Array<Uri>>? = null

    companion object {
        private const val FILE_CHOOSER_REQUEST_CODE = 1001
    }

    @Volatile
    private var tiltSteerValue: Float = 0f

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        // 여성 음성(TTS) 엔진 초기화 제거 (순수 자동차 엔진·드리프트·효과음만 재생)
        sensorManager = getSystemService(Context.SENSOR_SERVICE) as? SensorManager
        accelSensor = sensorManager?.getDefaultSensor(Sensor.TYPE_GRAVITY)
            ?: sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

        webView = WebView(this).apply {
            setBackgroundColor(0xFF0D1B2A.toInt())
            isVerticalScrollBarEnabled = false
            isHorizontalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_NEVER

            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                mediaPlaybackRequiresUserGesture = false
                allowFileAccess = true
                allowContentAccess = true
                cacheMode = WebSettings.LOAD_NO_CACHE
                setSupportZoom(false)
                builtInZoomControls = false
                displayZoomControls = false
                useWideViewPort = true
                loadWithOverviewMode = true
            }

            webViewClient = WebViewClient()
            webChromeClient = object : WebChromeClient() {
                override fun onShowFileChooser(
                    webView: WebView?,
                    filePathCallback: ValueCallback<Array<Uri>>?,
                    fileChooserParams: FileChooserParams?
                ): Boolean {
                    fileUploadCallback?.onReceiveValue(null)
                    fileUploadCallback = filePathCallback
                    return try {
                        val intent = Intent(Intent.ACTION_GET_CONTENT).apply {
                            addCategory(Intent.CATEGORY_OPENABLE)
                            type = "image/*"
                            putExtra(
                                Intent.EXTRA_ALLOW_MULTIPLE,
                                fileChooserParams?.mode == FileChooserParams.MODE_OPEN_MULTIPLE
                            )
                        }
                        startActivityForResult(
                            Intent.createChooser(intent, "레이서 얼굴 사진 선택"),
                            FILE_CHOOSER_REQUEST_CODE
                        )
                        true
                    } catch (_: Exception) {
                        fileUploadCallback = null
                        false
                    }
                }
            }
            addJavascriptInterface(KartBridge(), "AndroidBridge")
        }

        setContentView(webView)
        webView.post { hideSystemUI() }
        webView.loadUrl("file:///android_asset/index.html")

        // 앱 시작 시 백그라운드 자동 업데이트 확인 (inanimals-1977.web.app / GitHub)
        AppUpdater.checkOnStartup(this)
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == FILE_CHOOSER_REQUEST_CODE) {
            val callback = fileUploadCallback
            fileUploadCallback = null
            if (resultCode == RESULT_OK && data != null) {
                val clip = data.clipData
                val results: Array<Uri>? = when {
                    clip != null && clip.itemCount > 0 -> {
                        Array(clip.itemCount) { idx -> clip.getItemAt(idx).uri }
                    }
                    data.data != null -> arrayOf(data.data!!)
                    else -> null
                }
                callback?.onReceiveValue(results)
            } else {
                callback?.onReceiveValue(null)
            }
        }
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        webView.evaluateJavascript("if(window.onBackKey) window.onBackKey();", null)
    }

    override fun onInit(status: Int) {
        // 여성 음성(TTS) 완전 비활성화
        ttsReady = false
    }

    inner class KartBridge {
        @JavascriptInterface
        fun speak(text: String, flush: Boolean) {
            // 여성 음성(TTS) 출력 완전 차단
        }

        @JavascriptInterface
        fun vibrate(ms: Long) {
            try {
                val duration = ms.coerceIn(10L, 400L)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                    val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                    vm?.defaultVibrator?.vibrate(
                        VibrationEffect.createOneShot(duration, VibrationEffect.DEFAULT_AMPLITUDE)
                    )
                } else {
                    @Suppress("DEPRECATION")
                    val v = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        v?.vibrate(VibrationEffect.createOneShot(duration, VibrationEffect.DEFAULT_AMPLITUDE))
                    } else {
                        @Suppress("DEPRECATION")
                        v?.vibrate(duration)
                    }
                }
            } catch (_: Exception) {
            }
        }

        @JavascriptInterface
        fun getTiltSteer(): Float {
            return tiltSteerValue
        }

        @JavascriptInterface
        fun checkUpdate() {
            runOnUiThread {
                AppUpdater.checkManual(this@MainActivity)
            }
        }

        @JavascriptInterface
        fun getAppVersion(): String {
            return AppUpdater.installedVersionName(this@MainActivity)
        }

        @JavascriptInterface
        fun closeApp() {
            runOnUiThread {
                tts?.stop()
                finish()
            }
        }
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (event == null) return
        val y = event.values[1]
        val normalized = (y / 4.8f).coerceIn(-1f, 1f)
        tiltSteerValue = tiltSteerValue * 0.7f + normalized * 0.3f
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    override fun onResume() {
        super.onResume()
        webView.post { hideSystemUI() }
        webView.onResume()
        webView.resumeTimers()
        webView.evaluateJavascript("if(window.onAppResume) window.onAppResume();", null)
        accelSensor?.let {
            sensorManager?.registerListener(this, it, SensorManager.SENSOR_DELAY_GAME)
        }
        AppUpdater.resumePendingInstallIfAllowed(this)
    }

    override fun onPause() {
        sensorManager?.unregisterListener(this)
        tts?.stop()
        try {
            webView.evaluateJavascript("if(window.onAppPause) window.onAppPause();", null)
            webView.onPause()
            webView.pauseTimers()
        } catch (_: Exception) {
        }
        super.onPause()
    }

    override fun onStop() {
        tts?.stop()
        try {
            webView.evaluateJavascript("if(window.onAppPause) window.onAppPause();", null)
            webView.onPause()
            webView.pauseTimers()
        } catch (_: Exception) {
        }
        super.onStop()
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus) {
            webView.post { hideSystemUI() }
        }
    }

    private fun hideSystemUI() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                window.insetsController?.let { controller ->
                    controller.hide(WindowInsets.Type.statusBars() or WindowInsets.Type.navigationBars())
                    controller.systemBarsBehavior =
                        WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                }
            } else {
                @Suppress("DEPRECATION")
                window.decorView.systemUiVisibility = (
                    View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        or View.SYSTEM_UI_FLAG_FULLSCREEN
                    )
            }
        } catch (_: Exception) {
        }
    }

    override fun onDestroy() {
        tts?.stop()
        tts?.shutdown()
        webView.destroy()
        super.onDestroy()
    }
}
