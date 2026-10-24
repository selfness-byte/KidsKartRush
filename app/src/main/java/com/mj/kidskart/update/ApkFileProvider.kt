package com.mj.kidskart.update

import android.content.ContentProvider
import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.MatrixCursor
import android.net.Uri
import android.os.ParcelFileDescriptor
import android.provider.OpenableColumns
import java.io.File
import java.io.FileNotFoundException

/**
 * 외부 AndroidX 의존성 없이 앱 캐시 내 업데이트 APK 파일을
 * Android 패키지 인스톨러에 content:// URI로 안전하게 전달하는 전용 ContentProvider.
 */
class ApkFileProvider : ContentProvider() {

    override fun onCreate(): Boolean = true

    override fun openFile(uri: Uri, mode: String): ParcelFileDescriptor? {
        val ctx = context ?: throw FileNotFoundException("Context is null")
        val fileName = uri.lastPathSegment ?: throw FileNotFoundException("Missing file name")
        val file = File(File(ctx.cacheDir, "updates"), fileName)
        if (!file.exists()) throw FileNotFoundException("APK not found: ${file.absolutePath}")
        return ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
    }

    override fun query(
        uri: Uri,
        projection: Array<out String>?,
        selection: String?,
        selectionArgs: Array<out String>?,
        sortOrder: String?
    ): Cursor {
        val ctx = context ?: return MatrixCursor(emptyArray())
        val fileName = uri.lastPathSegment ?: "KidsKartRush.apk"
        val file = File(File(ctx.cacheDir, "updates"), fileName)
        val cols = projection ?: arrayOf(OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE)
        val values = arrayOfNulls<Any>(cols.size)
        for (i in cols.indices) {
            when (cols[i]) {
                OpenableColumns.DISPLAY_NAME -> values[i] = file.name
                OpenableColumns.SIZE -> values[i] = if (file.exists()) file.length() else 0L
            }
        }
        return MatrixCursor(cols, 1).apply { addRow(values) }
    }

    override fun getType(uri: Uri): String = "application/vnd.android.package-archive"

    override fun insert(uri: Uri, values: ContentValues?): Uri? = null
    override fun delete(uri: Uri, selection: String?, selectionArgs: Array<out String>?): Int = 0
    override fun update(uri: Uri, values: ContentValues?, selection: String?, selectionArgs: Array<out String>?): Int = 0

    companion object {
        fun getUriForFile(context: Context, file: File): Uri {
            return Uri.parse("content://${context.packageName}.fileprovider/updates/${file.name}")
        }
    }
}
