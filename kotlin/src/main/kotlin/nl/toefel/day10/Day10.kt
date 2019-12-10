package nl.toefel.day10

import java.io.File
import kotlin.math.abs
import kotlin.math.max

data class Point(val x: Int, val y: Int) {
    operator fun minus(other: Point): Point = Point(x - other.x, y - other.y)
    operator fun plus(other: Point): Point = Point(x + other.x, y + other.y)
    fun toSmallestUnitByGcd(): Point {
        val divisor = abs(gcd(x, y))
        return Point(x / divisor, y / divisor)
    }

    override fun toString(): String = "($x,$y)"

    val radian = 0.0174533
    fun angleInDegrees(origin: Point): Double {
        val delta = (this - origin)
        val angle = Math.atan2(delta.x * 1.0, -1.0 * delta.y) / radian
//        return angle
        return if (angle < 0) 360 + angle else angle
    }
}

fun gcd(a: Int, b: Int): Int = if (b == 0) a else gcd(b, a % b)

data class Grid(val width: Int, val height: Int, val source: Point, val asteroidsInSight: MutableMap<Point, Boolean>) {
    fun removeInvisibleAsteriods() {
        for (distance in 1..max(width, height)) {
            val points = getPointsForDistance(distance)
            if (points.isEmpty()) break // reaching outside the grid
            val asteroidsNearby = points.filter { asteroidsInSight.containsKey(it) }
            asteroidsNearby.forEach { blockSightLine(source, it) }
        }
    }

    fun countVisisbleAsteriods() = asteroidsInSight.count { it.value }

    private fun blockSightLine(source: Point, to: Point) {
        val delta = (to - source).toSmallestUnitByGcd()
        generateSequence(to + delta) { current -> current + delta }
            .takeWhile { inGrid(it) }
            .filter { asteroidsInSight.containsKey(it) }
            .forEach { asteroidsInSight[it] = false }
    }

    private fun getPointsForDistance(distance: Int): List<Point> {
        val pointsOverXAxis = (source.x - distance..source.x + distance)
            .map { listOf(Point(it, source.y - distance), Point(it, source.y + distance)) }
            .flatten()

        val pointsOverYAxis = (source.y - distance + 1 until source.y + distance)
            .map { listOf(Point(source.x - distance, it), Point(source.x + distance, it)) }
            .flatten()

        // only include points present in the grid
        return (pointsOverXAxis + pointsOverYAxis).filter { inGrid(it) }
    }

    private fun inGrid(it: Point) = it.x in 0..width && it.y in 0..height

    fun print() {
        (0 until height)
            .forEach { y ->
                (0 until width).forEach { x ->
                    when {
                        Point(x, y) == source -> print("o")
                        asteroidsInSight[Point(x, y)] == null -> print(".")
                        asteroidsInSight[Point(x, y)] == true -> print("#")
                        asteroidsInSight[Point(x, y)] == false -> print("*")
                    }
                }
                println()
            }
    }
}

fun main() {
    val center = Point(5, 5)
    val point = Point(6, 4)

    println(point.angleInDegrees(center))

    println(Point(0, 2).angleInDegrees(center))
    println(Point(1, 2).angleInDegrees(center))
    println(Point(2, 2).angleInDegrees(center))
    println(Point(2, 1).angleInDegrees(center))
    println(Point(2, 0).angleInDegrees(center))
    println(Point(2, -1).angleInDegrees(center))
    println(Point(2, -2).angleInDegrees(center))
    println(Point(1, -2).angleInDegrees(center))
    println(Point(1, -2).angleInDegrees(center))
    println(Point(0, -2).angleInDegrees(center))
    println(Point(-1, -2).angleInDegrees(center))
    println(Point(-2, -2).angleInDegrees(center))
    println(Point(-2, -1).angleInDegrees(center))
    println(Point(-2, 0).angleInDegrees(center))
    println(Point(-2, 1).angleInDegrees(center))
    println(Point(-2, 2).angleInDegrees(center))



//    return;
    val inputLines = File(ClassLoader.getSystemResource("day10-input.txt").file).readLines()
    val asteroids = inputLines
        .mapIndexed { y, row -> row.mapIndexed { x, col -> if (col == '#') Point(x, y) else null } }
        .flatten()
        .filterNotNull()

    val width = inputLines[0].length
    val height = inputLines.size

    val asteroidsMap = asteroids.map { it to true }.toMap()

    println(gcd(5, 2))

    val grid = asteroids.map { asteroid ->
        val grid = Grid(width, height, asteroid, asteroidsMap.minus(asteroid).toMutableMap())
        grid.removeInvisibleAsteriods()
        grid
    }.maxBy { it.countVisisbleAsteriods() }!!

    println("Best asteriod ${grid.source}. Has visibility over: ${grid.countVisisbleAsteriods()} asteroids")
    grid.print()

    val asteroids2 = grid.asteroidsInSight.filterValues { it }.keys.minus(grid.source)
    val asteriod200 = asteroids2.sortedBy { it.angleInDegrees(grid.source) }[199]
    println("part 2 = ${asteriod200.x * 100 + asteriod200.y}")
}
