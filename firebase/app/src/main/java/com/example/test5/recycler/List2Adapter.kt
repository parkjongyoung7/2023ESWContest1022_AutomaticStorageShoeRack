package com.example.test5.recycler
import android.content.Context
import android.content.Intent
import android.media.Image
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.constraintlayout.widget.ConstraintSet.Layout
import androidx.recyclerview.widget.RecyclerView
import com.example.test5.R
import com.example.test5.util.ItemTouchHelperListener
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AlertDialog
import com.example.test5.LoadingActivity2
import com.example.test5.MainActivity
import com.example.test5.MyApplication
import com.google.firebase.ktx.Firebase

// ListAcivity2의 recycleview의 adapter
class List2Adapter(val context: Context,
                   val shoeList: MutableList<String>, val idList: MutableList<String>, val statusList:MutableList<Boolean?>)
    : RecyclerView.Adapter<RecyclerViewHolder>(){

    // 뷰 초기화하는 메소드
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.existing_item, parent, false)
        return RecyclerViewHolder(view)
    }

    // 항목 초기화
    override fun onBindViewHolder(holder: RecyclerViewHolder, position: Int) {

        // 뷰홀더에 shoes name 정보가 바인딩 되도록 함
        holder.onBind(shoeList[position])
        // 각 신발 layout 클릭시 실행할 기능. Main 화면으로 돌아감

        holder.ClickView.setOnClickListener {
            // 신발이 없을 때만 고를 수 있도록 함.
            if (statusList[position] == false){
                // Firestore 필드 변수 값 변경
                MyApplication.db.collection("signal")
                    .document("sign_question")
                    .update("which_shoe", idList[position])
                MyApplication.db.collection("signal")
                    .document("sign_question")
                    .update("sign_new","select")
                Thread.sleep(1000) // 업데이트 완료 될때까지 대기
                //Loadingactivity2 로 이동 <- firestore가 업데이트 될때까지 기다리기 위함
                val context = holder.itemView.context
                val intent = Intent(context, LoadingActivity2::class.java)
                context.startActivity(intent)
            }
            else{
                // 신발이 이미 보관되어있으면, 오류 메세지를 보낸다.
                Toast.makeText(context, "이미 보관중인 신발입니다", Toast.LENGTH_SHORT).show()
            }
        }

    }

    // 리스트의 사이즈를 나타내는 함수.
    override fun getItemCount(): Int {
        return shoeList.size
    }


}
class RecyclerViewHolder(view: View): RecyclerView.ViewHolder(view) {
    val shoeView = view.findViewById<TextView>(R.id.shoe_view)
    val ClickView = view.findViewById<LinearLayout>(R.id.selectLayout)


    private var oldName: String? = null
    // 뷰에 값 셋팅
    fun onBind(name: String) {
        // 신발 이름을 표시하고, 수정 버튼 클릭 시 신발 이름을 수정할 수 있도록 한다.
        shoeView.text = name
//        ClickView.setOnClickListener{
//
//        }

    }


}