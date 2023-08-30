package com.example.test5.util

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.test5.R

// ItemTouchHelper.Callback 클래스를 상속받는 클래스
class ItemTouchHelperCallback(val listener: ItemTouchHelperListener, val context: Context) : ItemTouchHelper.Callback() {
    override fun getMovementFlags(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder
    ): Int {
        // 드래그 방향
        val dragFlags = ItemTouchHelper.UP or ItemTouchHelper.DOWN
        // 스와이프 방향
        val swipeFlags = ItemTouchHelper.LEFT
        // 이동을 만드는 메소드
        return makeMovementFlags(dragFlags, swipeFlags)
    }
    // 드래그된 item을 이전 위치에서 새로운 위치로 옮길 때 호출
    override fun onMove(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        target: RecyclerView.ViewHolder
    ): Boolean {
        // 리스너의 onMove 메소드 호출
        return listener.onItemMove(viewHolder.adapterPosition, target.adapterPosition)
    }

    // 사용자에 의해 swipe될 때 호출
    override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
        // 리스너의 onItemSwipe 메소드 호출
        listener.onItemSwipe(viewHolder.adapterPosition)
    }

    //swipe할 때 빨간색 그림이 나오도록 하는 함수
    override fun onChildDraw(
        c: Canvas,
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        dX: Float,
        dY: Float,
        actionState: Int,
        isCurrentlyActive: Boolean
    ) {
        val icon: Bitmap
        if (actionState == ItemTouchHelper.ACTION_STATE_SWIPE){
            val itemView = viewHolder.itemView
            val height = (itemView.bottom - itemView.top).toFloat()
            val width = height/4
            val paint = Paint() // Canvas라는 객체를 사용해서 그림을 그리기 위해, paint라는 객체를 하나 만들어줌.
            if (dX < 0){
                paint.color = Color.parseColor("#ff0000") // 스와프시 해당 아이템 공간에 빨간색이 나타나도록 함.
                val background = RectF(itemView.right.toFloat() + dX, itemView.top.toFloat(), itemView.right.toFloat(), itemView.bottom.toFloat())
                c.drawRect(background, paint)


                icon = BitmapFactory.decodeResource(context.resources, R.drawable.ic_menu_delete)
                val iconDst = RectF(itemView.right.toFloat() - 3 * width, itemView.top.toFloat() + width, itemView.right.toFloat() - width, itemView.bottom.toFloat() - width)
                c.drawBitmap(icon, null, iconDst, null)


            }
        }
        super.onChildDraw(
            c,
            recyclerView,
            viewHolder, dX, dY, actionState, isCurrentlyActive)
    }
}