package com.example.test5

import android.content.ClipData.Item
import android.os.Build.VERSION_CODES.M
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.Toast
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
//import com.example.test5.databinding.ActivityListBinding
//import com.example.test5.databinding.ActivityMainBinding
import com.example.test5.model.ItemData
import com.example.test5.recycler.MyAdapter
import com.example.test5.util.ItemTouchHelperCallback
import com.example.test5.util.ItemTouchHelperListener
import com.example.test5.recycler.ListAdapter
import com.google.android.play.integrity.internal.j
import java.util.Collections


class ListActivity : AppCompatActivity() {
    lateinit var recyclerView: RecyclerView
    lateinit var list:ArrayList<String>
    lateinit var idList:ArrayList<String>
    lateinit var itemList:MutableList<ItemData>
    lateinit var statusList:ArrayList<Boolean?>
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_list)
        recyclerView = findViewById(R.id.listRecyclerView)

        //binding.listRecyclerView.visibility= View.VISIBLE
        recyclerViewInit()

        val confirmButton: Button = findViewById(R.id.confirmButton)
        confirmButton.setOnClickListener {
            // 저장 버튼이 눌렸을 때 해야할 일
            saveData()

            Toast.makeText(this, "저장되었습니다.", Toast.LENGTH_SHORT).show()

        }
    }

    private fun recyclerViewInit() {

        MyApplication.db.collection("shoes")
            .orderBy("order")
            .get()
            .addOnSuccessListener { result ->
                itemList = mutableListOf<ItemData>() // itemList 초기화
                for (document in result) {
                    val item = document.toObject(ItemData::class.java)
                    item.docId = document.id
                    itemList.add(item)
                    //Collections.swap(itemList,0,1)
                }

                //val name = itemList.get(1).shoe_name
                val num = itemList.size
                list = ArrayList<String>()
                for(i in 0 until num) {
                    val name = itemList.get(i).shoe_name
                    list.add(name.toString())
                }
                //Collections.swap(itemList,0,1)
                idList = ArrayList<String>()
                for(i in 0 until num) {
                    val id = itemList.get(i).docId
                    idList.add(id.toString())
                }

                statusList = ArrayList<Boolean?>()
                for(i in 0 until num) {
                    val status = itemList.get(i).shelf_status
                    statusList.add(status)
                }

                // 어댑터
                val adapter = ListAdapter(this,list, idList, statusList)

                recyclerView.adapter = adapter

                // 리스너를 구현한 Adapter 클래스를 Callback 클래스의 생성자로 지정
                val itemTouchHelperCallback = ItemTouchHelperCallback(adapter, this)

                // ItemTouchHelper의 생성자로 ItemTouchHelper.Callback 객체 셋팅
                val helper = ItemTouchHelper(itemTouchHelperCallback)
                // RecyclerView에 ItemTouchHelper 연결
                helper.attachToRecyclerView(recyclerView)
            }


    }

    //저장 버튼이 눌릴 시 데이터를 파이어 베이스에 저장
    private fun saveData() {

        for (i in 0 until itemList.size) {
            MyApplication.db.collection("shoes")
                .document(itemList.get(i).docId.toString())
                .update("remain", false)
        }
        /*
        Toast.makeText(
            this,
            "list.size: ${list.size}, itemList.size: ${itemList.size}",
            Toast.LENGTH_SHORT
        ).show()
        Toast.makeText(
            this,
            "0: ${itemList.get(0).docId.toString()}, 1: ${itemList.get(1).docId.toString()}",
            Toast.LENGTH_SHORT
        ).show()

         */
        for (i in 0 until list.size) {
            for (j in 0 until itemList.size) {
                if (idList[i] == itemList.get(j).docId) {
                    MyApplication.db.collection("shoes")
                        .document(itemList.get(j).docId.toString())
                        .update(
                            mapOf(
                                "shoe_name" to list[i],
                                "order" to i,
                                "remain" to true
                            )
                        )
                }
            }
        }

        if (list.size < itemList.size) {
            MyApplication.db.collection("shoes")
                .whereEqualTo("remain", false)
                .get()
                .addOnSuccessListener { querySnapshot ->
                    for (document in querySnapshot) {
                        val documentRef = MyApplication.db.collection("shoes").document(document.id)
                        documentRef.delete()

                    }

                }

        }
    }}

