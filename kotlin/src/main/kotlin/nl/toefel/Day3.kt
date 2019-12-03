package nl.toefel

import java.io.File
import kotlin.math.absoluteValue

data class Point(val x: Int, val y: Int) {
    fun repeat(count: Int): List<Point> = (0 until count).map { this }
    operator fun plus(other: Point): Point = Point(x + other.x, y + other.y)
    fun manhattanDistanceTo(to: Point): Int = (x - to.x).absoluteValue + (y - to.y).absoluteValue
}

val origin = Point(0, 0)

fun main() {
    val (wire1, wire2) = File(ClassLoader.getSystemResource("day3-input.txt").file).readLines().map { it.split(",") }
    val path1: List<Point> = getCoordinatePath(wire1)
    val path2: List<Point> = getCoordinatePath(wire2)
    val crossings = path1.intersect(path2).minus(origin)
    val closestManhattanDistance = crossings.map { origin.manhattanDistanceTo(it) }.min()!!
    println("part 1 = $closestManhattanDistance")

    val closestCrossingInSteps = crossings.map { crossing -> path1.indexOf(crossing) + path2.indexOf(crossing) }.min()!!
    println("part 2 = $closestCrossingInSteps")
}

fun getCoordinatePath(wire: List<String>): List<Point> = wire
    .map {
        val times = it.substring(1).toInt()
        when (it[0]) {
            'U' -> Point(0, -1).repeat(times)
            'D' -> Point(0, 1).repeat(times)
            'L' -> Point(-1, 0).repeat(times)
            'R' -> Point(1, 0).repeat(times)
            else -> throw IllegalStateException("unknown instruction $it")
        }
    }
    .flatten()
    // mutable list for performance
    .fold(mutableListOf(origin)) { acc: MutableList<Point>, next: Point -> acc.add(acc.last() + next); acc }