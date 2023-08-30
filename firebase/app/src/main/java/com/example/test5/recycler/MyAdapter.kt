package com.example.test5.recycler

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.Toast
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide

import com.example.test5.LoadingActivity
import com.example.test5.MyApplication
import com.example.test5.model.ItemData
import com.example.test5.databinding.ItemMainBinding
import com.example.test5.util.ItemTouchHelperListener
import com.google.firebase.firestore.FirebaseFirestore
import java.util.Collections
import java.util.Date

// 원래꺼
//class MyViewHolder(val binding: ItemMainBinding) : RecyclerView.ViewHolder(binding.root)

//바꾼거
class MyViewHolder(val binding: ItemMainBinding) : RecyclerView.ViewHolder(binding.root)

class MyAdapter(val context: Context, val itemList: MutableList<ItemData>): RecyclerView.Adapter<MyViewHolder>(){

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        return MyViewHolder(ItemMainBinding.inflate(layoutInflater))
    }


    //리스트의 사이즈
    override fun getItemCount(): Int {
        return itemList.size
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        val data = itemList.get(position)

        holder.binding.run {
            //itemEmailView.text=data.email
            //itemDateView.text=data.date
            itemContentView.text = data.shoe_name

        }
        if (data.shelf_status == true) {
            holder.binding.itemExistenceView.text = "보관중"
            holder.binding.itemExistenceView.setTextColor(Color.GREEN)
        } else {
            holder.binding.itemExistenceView.text = "미보관"
            holder.binding.itemExistenceView.setTextColor(Color.RED)
        }
        //스토리지 이미지 다운로드........................
        val imgRef = MyApplication.storage.reference.child("shoeImages/${data.docId}.jpg")
        imgRef.downloadUrl.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                Glide.with(context)
                    .load(task.result)
                    .into(holder.binding.itemImageView)
            }

        }
        //버튼 로직 구현
        holder.binding.startRemove.setOnClickListener {
            //신발이 없다면 Toast 띄우기
            if (data.shelf_status == false) {
                Log.d("TM", "실행되었음")
                Toast.makeText(
                    holder.binding.startRemove.context,
                    "보관 중이지 않습니다",
                    Toast.LENGTH_SHORT
                ).show()
            }
            //신발이 있다면
            else {
                //우선 파이어 베이스 접근하도록 함
                val db = FirebaseFirestore.getInstance()
                val signalRef = db.collection("signal").document("from_app_to_RPi")
                //어떤 신발을 선택했는지 DoCName에 저장
                signalRef.update("DocName", data.docId)
                    .addOnSuccessListener {
                        // 업데이트 성공 시 실행되는 코드
                    }
                    .addOnFailureListener { e ->
                        // 업데이트 실패 시 실행되는 코드
                    }
                //이후 request flied를 true로 바꾸고 로딩창을 띄우는 activity로 들어감
                signalRef.update("request", true)
                    .addOnSuccessListener {
                        // 업데이트 성공 시 실행되는 코드
                        val intent = Intent(context, LoadingActivity::class.java)
                        context.startActivity(intent)
                    }
                    .addOnFailureListener { e ->
                        // 업데이트 실패 시 실행되는 코드
                    }
            }
            holder.binding.startRemove.setOnClickListener {
                //신발이 없다면 Toast 띄우기
                if (data.shelf_status == false) {
                    Log.d("TM", "실행되었음")
                    Toast.makeText(
                        holder.binding.startRemove.context,
                        "보관 중이지 않습니다",
                        Toast.LENGTH_SHORT
                    ).show()
                }
                //신발이 있다면
                else {
                    //우선 파이어 베이스 접근하도록 함
                    val db = FirebaseFirestore.getInstance()
                    val signalRef = db.collection("signal").document("from_app_to_RPi")
                    //어떤 신발을 선택했는지 DoCName에 저장
                    signalRef.update("DocName", data.docId)
                        .addOnSuccessListener {
                            // 업데이트 성공 시 실행되는 코드
                        }
                        .addOnFailureListener { e ->
                            // 업데이트 실패 시 실행되는 코드
                        }
                    //이후 request flied를 true로 바꾸고 로딩창을 띄우는 activity로 들어감
                    signalRef.update("request", true)
                        .addOnSuccessListener {
                            // 업데이트 성공 시 실행되는 코드
                            val intent = Intent(context, LoadingActivity::class.java)
                            context.startActivity(intent)
                        }
                        .addOnFailureListener { e ->
                            // 업데이트 실패 시 실행되는 코드
                        }
                }
            }

        }
    }
}

