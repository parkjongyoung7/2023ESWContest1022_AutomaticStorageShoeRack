package com.example.test5

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.google.firebase.firestore.DocumentReference
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage

class SelectActivity: AppCompatActivity() {

    private lateinit var button1 :Button
    private lateinit var button2 :Button
    private val firestore: FirebaseFirestore =
        FirebaseFirestore.getInstance()  // firestore instance 받아옴
    private val sign_new_DocRef: DocumentReference = firestore.collection("signal")
        .document("sign_question")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_select)
        button1 = findViewById(R.id.button1)
        button2 = findViewById(R.id.button2)

        //새로운 신발 등록하기
        button1.setOnClickListener {
            val updates = hashMapOf<String, Any>(
                "sign_new" to "Yes" // 변경할 "sign_new" 필드의 새로운 값
            )

            sign_new_DocRef.update(updates)
                .addOnSuccessListener {
                    // 업데이트 성공
                }
                .addOnFailureListener { error ->
                    // 업데이트 실패 처리
                }
            // 업데이트 수행 후 MainActivity 로 들어감
            //Toast.makeText(this,"등록되었습니다.",Toast.LENGTH_SHORT).show()
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)

        }
        //기존 신발이었던 것
        button2.setOnClickListener {
            val updates = hashMapOf<String, Any>(
                "sign_new" to "exist" // 변경할 "sign_new" 필드의 새로운 값
            )

            sign_new_DocRef.update(updates)
                .addOnSuccessListener {
                    // 업데이트 성공
                    Thread.sleep(500) // firestore에서 문서 삭제가 완료될때 까지 잠시 대기

                }
                .addOnFailureListener { error ->
                    // 업데이트 실패 처리
                }
            //기존 신발 선택 화면 (ListActivity2)

            val intent = Intent(this, ListActivity2::class.java)
            startActivity(intent)

        }

        val receivedValue = intent.getStringExtra("key") ?: ""
        Log.d("name", "name 이거: ${receivedValue}")
        loadImageFromFirebaseStorage(receivedValue)
    }
    // Firebase Storage에서 이미지를 가져와서 ImageView에 표시하는 함수
    private fun loadImageFromFirebaseStorage(imagePath: String) {
        // Firebase Storage의 이미지 위치를 가리키는 StorageReference 생성
        val storageReference = FirebaseStorage.getInstance().reference.child("shoeImages/"+imagePath)

        // 이미지 다운로드 및 표시
        val imageView: ImageView = findViewById(R.id.newImage)

        // StorageReference에서 이미지 다운로드 URL 가져오기
        storageReference.downloadUrl.addOnSuccessListener { uri ->
            // Glide 또는 Picasso 등의 라이브러리를 사용하여 이미지를 다운로드하고 ImageView에 설정
            Glide.with(this)
                .load(uri)
                .into(imageView)
        }.addOnFailureListener { exception ->
            // 이미지 다운로드 실패 시 처리할 내용
            Toast.makeText(this, "이미지 다운로드 실패: ${exception.message}", Toast.LENGTH_SHORT).show()
        }
    }

}