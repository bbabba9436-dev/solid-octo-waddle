package com.example.workbook

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.io.InputStreamReader

@Serializable
data class QAPair(
    val id: Int,
    val question: String,
    val answer: String
)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pairs = loadPairs()
        setContent {
            MaterialTheme {
                LazyColumn(modifier = Modifier.fillMaxSize()) {
                    items(pairs.size) { index ->
                        val item = pairs[index]
                        var showAnswer by remember { mutableStateOf(false) }
                        Column {
                            Text(text = item.question)
                            Button(onClick = { showAnswer = !showAnswer }) {
                                Text(if (showAnswer) "Hide Answer" else "Show Answer")
                            }
                            if (showAnswer) {
                                Text(text = item.answer)
                            }
                        }
                    }
                }
            }
        }
    }

    private fun loadPairs(): List<QAPair> {
        val input = assets.open("pairs.json")
        val text = InputStreamReader(input).readText()
        return Json.decodeFromString(text)
    }
}

