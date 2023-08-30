package com.example.test5.recycler
import android.content.Context
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
import com.example.test5.MyApplication

// Listener 인터페이스를 구현
class ListAdapter(val context: Context,
                  val nameList: MutableList<String>, val idList: MutableList<String>, val statusList: MutableList<Boolean?>)
    : RecyclerView.Adapter<ListAdapter.RecyclerViewHolder>(), ItemTouchHelperListener {
    //private var oldName: String? = null
    //private var newName: String? = null
    // 뷰 초기화하는 메소드
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.sample_item, parent, false)
        return RecyclerViewHolder(view)
    }

    // 뷰홀더에 신발 문서 ID 와 신발 이름 리스트를 바인드
    override fun onBindViewHolder(holder: RecyclerViewHolder, position: Int) {
        holder.onBind(idList[position])
        holder.onBind(nameList[position])

    }

    // 리스트의 사이즈
    override fun getItemCount(): Int {
        return nameList.size
    }
    // 아이템을 드래그되면 호출되는 메소드. 리스트 순서를 바꾼다.
    override fun onItemMove(from_position: Int, to_position: Int): Boolean {
        val name = nameList[from_position]
        // 리스트 갱신
        nameList.removeAt(from_position)
        nameList.add(to_position, name)

        // id 리스트도 함께 갱신
        val id = idList[from_position]
        idList.removeAt(from_position)
        idList.add(to_position, id)

        //status 도 갱신
        val status = statusList[from_position]
        statusList.removeAt(from_position)
        statusList.add(to_position, status)

        // fromPosition에서 toPosition으로 아이템 이동 공지
        notifyItemMoved(from_position, to_position)
        return true
    }

    // 아이템 스와이프되면 호출되는 메소드
    override fun onItemSwipe( position: Int){
        // 리스트 아이템 삭제
        // 보관 중인 신발은 삭제 하지 못하도록 함.
        val name = nameList[position]
        val id = idList[position]
        val status = statusList[position]

        notifyItemMoved(position, position)
        nameList.removeAt(position)
        idList.removeAt(position)
        statusList.removeAt(position)
        // 아이템 삭제되었다고 공지
        notifyItemRemoved(position)

        // 보관 중인 신발일 경우. 메세지를 보낸다.
        if (status == true) {
            Toast.makeText(context, "보관중인 신발입니다. 빼고 진행해주세요.", Toast.LENGTH_SHORT).show()
            nameList.add(position, name)
            idList.add(position, id)
            statusList.add(position, status)
            notifyItemInserted(position)
        }

    }
    // ViewHolder 클래스
    inner class RecyclerViewHolder(view: View): RecyclerView.ViewHolder(view) {
        val nameView = view.findViewById<TextView>(R.id.name_view)
        val ClickView = view.findViewById<LinearLayout>(R.id.vhLayout)
        val modifyView = view.findViewById<ImageView>(R.id.modify_handle)

        private var oldName: String? = null
        // 뷰에 값 셋팅
        fun onBind(name: String) {
            // 신발 이름을 표시하고, 수정 버튼 클릭 시 신발 이름을 수정할 수 있도록 한다.
            nameView.text = name
            // 신발 이름 레이아웃을 클릭하면, 리스트 수정 방법을 알리는 알림을 구현
            ClickView.setOnClickListener{
                Snackbar.make(it, "이 항목을 옮기려면 위/아래로 드래고, 없애려면 왼쪽으로 밀어주세요.", Snackbar.LENGTH_SHORT).show()

            }

            // 수정 버튼을 누르면 신발 이름을 수정할 수 있도록 함.
            modifyView.setOnClickListener{
                showEditDialog(adapterPosition)
            }

        }

        // 신발 이름 수정 함수
        fun showEditDialog(position: Int) {
            val editText = EditText(itemView.context)
            editText.setText(nameView.text)
            oldName = nameView.text.toString()


            // 신발 이름 수정을 위한 작은 창을 띄움
            AlertDialog.Builder(itemView.context)
                .setTitle("신발 이름 수정")
                .setView(editText)
                .setPositiveButton("확인") { _, _ ->
                    val newName = editText.text.toString()
                    nameView.text = newName
                    nameList[position] = newName

                    // 수정된 데이터를 저장하고 RecyclerView를 업데이트할 수 있는 메서드 호출
                }
                .setNegativeButton("취소", null)
                .show()
        }
    }

}

