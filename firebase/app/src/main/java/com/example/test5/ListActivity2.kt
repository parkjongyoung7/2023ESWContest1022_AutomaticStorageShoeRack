package com.example.test5


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
import com.example.test5.recycler.List2Adapter
import com.example.test5.recycler.MyAdapter
import com.example.test5.util.ItemTouchHelperCallback
import com.example.test5.util.ItemTouchHelperListener
import com.example.test5.recycler.ListAdapter
import com.google.android.play.integrity.internal.j
import java.util.Collections

// ListActivity 2는 기존신발이 새로운 신발로 인식되었을 경우 기존신발을 선택할 수 있는 리스트를 화면에 출력
class ListActivity2 : AppCompatActivity() {
    lateinit var recyclerView: RecyclerView
    lateinit var list:ArrayList<String>
    lateinit var idList:ArrayList<String>
    lateinit var itemList:MutableList<ItemData>
    lateinit var statusList:ArrayList<Boolean?>
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_list2)
        recyclerView = findViewById(R.id.list2RecyclerView)
        recyclerViewInit()
    }

    private fun recyclerViewInit() {

        // firestore에서 "shoe" collection에 해당하는 정보들을 받아옴.itemList에다 저장
        MyApplication.db.collection("shoes")
            .orderBy("order") // 리스트 정렬
            .get()
            .addOnSuccessListener { result ->
                itemList = mutableListOf<ItemData>() // itemList 초기화
                for (document in result) {
                    val item = document.toObject(ItemData::class.java)
                    item.docId = document.id
                    itemList.add(item)
                    
                }

                val num = itemList.size
                list = ArrayList<String>()
                idList = ArrayList<String>()
                statusList = ArrayList<Boolean?>()
                //list 배열에 신발 이름 저장 


                for(i in 1 until num) { //새로 등록된 신발은 리스트에 추가하지 않음.
                    val name = itemList.get(i).shoe_name
                    val id = itemList.get(i).docId
                    val status = itemList.get(i).shelf_status
                    if (status == false) {
                        list.add(name.toString())
                        idList.add(id.toString())
                        statusList.add(status)
                    }
                }

                //idlist 배열에 신발 문서 Id 저장

                //for(i in 1 until num){//새로 등록된 신발은 리스트에 추가하지 않음.
                    //val id = itemList.get(i).docId
                    //idList.add(id.toString())
                //}

                //statusList 배열에 신발 상태 저장

                //for(i in 1 until num) {
                    //val status = itemList.get(i).shelf_status
                    //statusList.add(status)
                //}


                // 어댑터 지정
                val adapter = List2Adapter(this, list, idList, statusList)
                recyclerView.adapter = adapter


                MyApplication.db.collection("shoes")
                    .document(itemList.get(0).docId.toString())
                    .delete()




            }


    }

}