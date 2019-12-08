package nl.toefel

import java.io.File

fun main() {
    val input = File(ClassLoader.getSystemResource("day8-input.txt").file).readText()

    val width = 25
    val height = 6

    val layers = input
        .windowed(width, width, true)
        .windowed(height, height, true)

    val layerLeastZeros = layers.minBy { row -> row.sumBy { column -> column.count { it == '0' } } }!!
    val count1 = layerLeastZeros.sumBy { row -> row.count { column -> column == '1' } }
    val count2 = layerLeastZeros.sumBy { row -> row.count { column -> column == '2' } }

    println("part1 = count1($count1) * count2($count2) = ${count1 * count2}")
    println("part2 =")
    (0 until height).map { row ->
        (0 until width).map { col ->
            val color = layers.indices.map { layer -> layers[layer][row][col] }.first { it == '0' || it == '1' }
            if (color == '1') print("$color") else print(" ")
        }
        println()
    }

}
