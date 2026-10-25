plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.mj.kidskart"
    compileSdk = 35
    buildToolsVersion = "35.0.0"

    defaultConfig {
        applicationId = "com.mj.kidskart"
        minSdk = 24
        targetSdk = 35
        versionCode = 23
        versionName = "1.9.5"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    // 순수 Android SDK 내장 API만 사용하여 오프라인 빌드 속도 극대화 및 의존성 충돌 원천 차단
}
