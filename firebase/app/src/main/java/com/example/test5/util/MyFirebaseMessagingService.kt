package com.example.test5.util

import android.app.ActivityManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.localbroadcastmanager.content.LocalBroadcastManager
import com.example.test5.R
import com.example.test5.SelectActivity
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage


class MyFirebaseMessagingService : FirebaseMessagingService() {

    companion object {
        private const val CHANNEL_ID = "my_channel_id"
        private const val NOTIFICATION_ID = 1
    }
    private fun createNotificationChannel() {
        //버전 확인 후 알림 채널 생성
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "My Channel",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            val notificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }

    }
    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)

        // 수신된 메시지 처리
        //RPi에서 보내는 data는 사진의 이름이여야 함(이미지 띄우기 위해서)
        val picturename = remoteMessage.data["key1"]
        Log.d("FCM", "Received message: $picturename")

        // 수신된 데이터를 처리하는 추가적인 로직을 여기에 추가할 수 있습니다.

        // 푸시 알림 표시
        if (isAppInForeground()) {
            // 앱이 포그라운드에 있을 때는 직접 알림을 표시
            showNotification(picturename)
        } else {
            // 앱이 백그라운드에 있을 때는 BroadcastReceiver를 통해 알림을 표시
            Log.d("fcm","back or ter")
            val intent = Intent("FCM_NOTIFICATION")
            intent.putExtra("notificationData", picturename)
            LocalBroadcastManager.getInstance(this).sendBroadcast(intent)
        }
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Log.d("FCM", "Refreshed token: $token")
        // 새로운 토큰이 생성되었을 때의 처리 로직을 여기에 추가할 수 있습니다.
    }

    //알림 생성 및 표시
    private fun showNotification(message: String?) {
        //intent 설정
        val intent = Intent(this, SelectActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
        intent.putExtra("key",message)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_MUTABLE
        )
        //알림 설정
        val notificationBuilder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("새로운 신발 감지!")
            .setContentText(message)
            .setSmallIcon(R.drawable.start)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)

        val notificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(NOTIFICATION_ID, notificationBuilder.build())
    }
    private fun isAppInForeground(): Boolean {
        val activityManager = getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        val appProcesses = activityManager.runningAppProcesses ?: return false

        for (appProcess in appProcesses) {
            if (appProcess.importance == ActivityManager.RunningAppProcessInfo.IMPORTANCE_FOREGROUND) {
                for (activeProcess in appProcess.pkgList) {
                    if (activeProcess == packageName) {
                        return true
                    }
                }
            }
        }

        return false
    }
}
//background에서 FCM을 받기 위한 class
class MyBroadcastReceiver : BroadcastReceiver() {
    //채널과 notification_id 생성
    companion object {
        const val CHANNEL_ID = "my_channel_id"
        const val NOTIFICATION_ID = 1
    }
    override fun onReceive(context: Context, intent: Intent) {

        val notificationData = intent.getStringExtra("notificationData")
        Log.d("FCM", "Received notification data: $notificationData")

        // 알림을 클릭했을 때 실행될 SelectActivity
        val launchIntent = Intent(context, SelectActivity::class.java)
        intent.putExtra("key",notificationData)
        launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        context.startActivity(launchIntent)

        showNotification(context, notificationData,CHANNEL_ID,NOTIFICATION_ID)
    }

    private fun showNotification(context: Context, message: String?, channelId: String,
                                 notificationId: Int) {

        val intent = Intent(context, SelectActivity::class.java)
        intent.putExtra("key",message)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)
        val pendingIntent = PendingIntent.getActivity(
            context, 0, intent,
            PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_MUTABLE
        )

        val notificationBuilder = NotificationCompat.Builder(context, channelId)
            .setContentTitle("새로운 신발 감지!")
            .setContentText(message)
            .setSmallIcon(R.drawable.start)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)


        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "My Channel",
                NotificationManager.IMPORTANCE_HIGH
            )
            notificationManager.createNotificationChannel(channel)
        }

        notificationManager.notify(NOTIFICATION_ID, notificationBuilder.build())
    }
}