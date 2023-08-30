package com.example.test5

import android.content.Intent
import android.content.IntentFilter
import android.os.Build.VERSION_CODES.S
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.KeyEvent
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.Toast
import androidx.core.content.ContextCompat.startActivity
import androidx.localbroadcastmanager.content.LocalBroadcastManager
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

import com.example.test5.databinding.ActivityMainBinding
import com.example.test5.model.ItemData
import com.example.test5.recycler.MyAdapter
import com.example.test5.util.ItemTouchHelperCallback
import java.util.Collections
import com.example.test5.ListActivity
import com.example.test5.util.MyBroadcastReceiver
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.messaging.FirebaseMessaging

class MainActivity : AppCompatActivity() {
    lateinit var binding: ActivityMainBinding
    private val broadcastReceiver = MyBroadcastReceiver()
    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        val filter = IntentFilter("FCM_NOTIFICATION")
        LocalBroadcastManager.getInstance(this).registerReceiver(broadcastReceiver, filter)
        //FCM을 받기 위한 토큰 생성
        FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                val token = task.result
                // 얻은 토큰의 정보를 라즈베리파이에게 전송해야 fcm이 가능하다
                // firestore를 얻은 토큰을 update
                val db = FirebaseFirestore.getInstance()
                val signalRef=db.collection("signal").document("from_app_to_RPi")
                signalRef
                    .update("fcm_token", token)
                    .addOnSuccessListener {
                        // 업데이트 성공 시 처리할 작업
                        println("fcm_token 업데이트 성공")
                    }
                    .addOnFailureListener { e ->
                        // 업데이트 실패 시 처리할 작업
                        println("fcm_token 업데이트 실패: $e")
                    }
            } else {
                // 토큰 얻기 실패 처리를 수행하세요.
            }
        }
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        //myCheckPermission(this) // 작성한 함수임
        binding.addFab.setOnClickListener {
            startActivity(Intent(this, ListActivity::class.java))
            /*
            if(MyApplication.checkAuth()){
                startActivity(Intent(this, ListActivity::class.java))
            }
            else {
                Toast.makeText(this, "인증진행해주세요 ",Toast.LENGTH_SHORT).show()
            }

             */


        }

        // 화면을 아래로 드래그 했을 경우 새로고침을 수행한다.
        val swipe : SwipeRefreshLayout = findViewById((R.id.swipeToRefresh))
        swipe.setOnRefreshListener {
            makeRecyclerView()
            swipe.isRefreshing = false
        }

    }
    override fun onDestroy() {
        super.onDestroy()
        LocalBroadcastManager.getInstance(this).unregisterReceiver(broadcastReceiver)
    }
    override fun onStart() {
        super.onStart()
        binding.logoutTextView.visibility= View.GONE
        binding.mainRecyclerView.visibility=View.VISIBLE
        makeRecyclerView()
    /*
        if(!MyApplication.checkAuth()){
            binding.logoutTextView.visibility= View.VISIBLE
            binding.mainRecyclerView.visibility=View.GONE
        }else {
            binding.logoutTextView.visibility= View.GONE
            binding.mainRecyclerView.visibility=View.VISIBLE
            makeRecyclerView()

        }

     */


    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        //startActivity(Intent(this, AuthActivity::class.java))
        //startActivity(Intent(this, ListActivity2::class.java))
        startActivity(Intent(this, SelectActivity::class.java))
        return super.onOptionsItemSelected(item)
    }

    // 뒤로가기 버튼이 눌렸을 때 앱이 종료되도록 함.
//    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
//        if (keyCode == KeyEvent.KEYCODE_BACK) {
//            // 뒤로가기 버튼을 눌렀을 때 앱 종료
//            finish()
//            return true
//        }
//        return super.onKeyDown(keyCode, event)
//    }
    override fun onBackPressed() {
        finish() // 액티비티 종료

    }


    // 기본 화면에 신발 목록을 recycleview로 나타냄
    private fun makeRecyclerView(){
        //
        MyApplication.db.collection("shoes")
            .orderBy("order")
            .get()
            .addOnSuccessListener { result->
                val itemList = mutableListOf<ItemData>()
                for(document in result){
                    val item = document.toObject(ItemData::class.java)
                    item.docId=document.id
                    itemList.add(item)
                    //Collections.swap(itemList,0,1)
                }


                //Collections.swap(itemList,0,1)
                //itemList.sortBy{it.num}
                binding.mainRecyclerView.layoutManager = LinearLayoutManager(this)
                binding.mainRecyclerView.adapter = MyAdapter(this, itemList)

                // 여기서 부터는 순서 바꾸기 해보기
                //val itemTouchHelperCallback = ItemTouchHelperCallback(MyAdapter(this,itemList))
                //  ItemTouchHelper의 생성자로 ItemTouchHelper.Callback객체 세팅
                //val helper = ItemTouchHelper(itemTouchHelperCallback)
                //helper.attachToRecyclerView(binding.mainRecyclerView)



            }
            .addOnFailureListener{exception->
                Log.d("yun","error..getting document..",exception)
                Toast.makeText(this,"서버 데이터 획득 실패",Toast.LENGTH_SHORT).show()

            }

    }



}