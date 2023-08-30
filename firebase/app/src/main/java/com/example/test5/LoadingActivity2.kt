package com.example.test5

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.firestore.DocumentReference
import com.google.firebase.firestore.FirebaseFirestore


class LoadingActivity2 :AppCompatActivity(){
    private val firestore: FirebaseFirestore =
        FirebaseFirestore.getInstance()  // firestore instance 받아옴
    private val SignNewSignal: DocumentReference = firestore.collection("signal")
        .document("sign_question")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_loading)
        observeSignNewValue()

    }
    private fun observeSignNewValue(){
        //sign_new field가 'No'로 바뀌면 종료 -> 업데이트 된 상태로 main으로 넘어간다
        SignNewSignal.addSnapshotListener { snapshot, error ->
            if (error != null) {
                // 오류 처리
                return@addSnapshotListener
            }

            val signnew = snapshot?.getString("sign_new")
            if (signnew == "No") {
                //이전 activity 종료 후 새로운 activiy 시작
                val intent = Intent(this, MainActivity::class.java)
                intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(intent)
                finish()
            }
        }
    }
}
