package nl.toefel.day12

import java.io.File

data class Point3D(val x: Int, val y: Int, val z: Int) {

}

typealias Vector = Point3D


fun main() {
    val initialCoordinates = File(ClassLoader.getSystemResource("day12-input.txt").file).readLines()
        .map { it.split(", |<|>|=".toRegex()) }
        .map { Point3D(it[2].toInt(), it[4].toInt(), it[6].toInt())}



    println(initialCoordinates)
}
