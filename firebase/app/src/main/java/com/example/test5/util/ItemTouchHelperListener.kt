package com.example.test5.util

// adapter 과 ItemTouchHelper.Callback 을 연결시켜주는 리스너
interface ItemTouchHelperListener {
    fun onItemMove(from_position: Int, to_position: Int): Boolean
    fun onItemSwipe(position: Int)
}