package com.example.test5

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.firestore.DocumentReference
import com.google.firebase.firestore.FirebaseFirestore
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

class LoadingActivity: AppCompatActivity() {

    private val firestore: FirebaseFirestore =
        FirebaseFirestore.getInstance()  // firestore instance 받아옴
    private val signalDocRef: DocumentReference = firestore.collection("signal")
        .document("from_app_to_RPi")


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_loading)
        observeRequestValue()
    }

    private fun observeRequestValue() {
        //변화읽음
        signalDocRef.addSnapshotListener { snapshot, error ->
            if (error != null) {
                // 오류 처리
                return@addSnapshotListener
            }

            val request = snapshot?.getBoolean("request")
            if (request == false) {
                // request 값이 false인 경우에 종료
                finish()
            }
        }

    }

}