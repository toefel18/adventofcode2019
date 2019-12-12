package nl.toefel.day12

import java.io.File
import kotlin.math.absoluteValue
import kotlin.math.sign

data class Point3D(val x: Int, val y: Int, val z: Int) {
    fun applyGravity(other: Point3D) = Point3D(
        x = other.x.compareTo(this.x).sign,
        y = other.y.compareTo(this.y).sign,
        z = other.z.compareTo(this.z).sign)

    operator fun plus(other: Point3D) = Point3D(this.x + other.x, this.y + other.y, this.z + other.z)
    fun energy(): Int = x.absoluteValue + y.absoluteValue + z.absoluteValue
    fun digitString() : String = x.toString().padStart(3) + y.toString().padStart(3) + z.toString().padStart(3)
}

data class Moon(val pos: Point3D, val velocity: Point3D) {
    fun applyGravity(others: List<Moon>): Moon {
        val newVelocity = others.map { pos.applyGravity(it.pos) }.reduce { acc, next -> acc + next } + velocity
        return Moon(pos + newVelocity, newVelocity)
    }

    fun totalEnergy() = pos.energy() * velocity.energy()
}

fun List<Moon>.print(step: Int) {
    println("Step $step=")
    forEach { println(it) }
}

fun main() {
    part1()
//    part2()
}

private fun part1() {
    val moons = File(ClassLoader.getSystemResource("day12-input.txt").file).readLines()
        .map { it.split(", |<|>|=".toRegex()) }
        .map { Moon(Point3D(it[2].toInt(), it[4].toInt(), it[6].toInt()), Point3D(0, 0, 0)) }

    var currentMoons = moons
//    currentMoons.print(0)

    (1..1000).forEach { step ->
        currentMoons = currentMoons.map { it.applyGravity(currentMoons.minus(it)) }
//        currentMoons.print(step)
    }

//    currentMoons.forEach { moon ->
//        val potentialEnergy = moon.pos.energy()
//        val kineticEnergy = moon.velocity.energy()
//        val total = moon.totalEnergy()
//        println("pot: $potentialEnergy  kin: $kineticEnergy  total: $total")
//    }

    println("Part 1 total energy in system: " + currentMoons.map { it.totalEnergy() }.sum())
}

val ZeroVelocity = Point3D(0,0,0)


fun List<Moon>.printVelocity(step: Int) {
    println("Step ${step.toString().padStart(10)} ${this.map { it.velocity.digitString() }.joinToString()}")
    forEach { println(it) }
}

private fun part2() {
    val moons = File(ClassLoader.getSystemResource("day12-test-input.txt").file).readLines()
        .map { it.split(", |<|>|=".toRegex()) }
        .map { Moon(Point3D(it[2].toInt(), it[4].toInt(), it[6].toInt()), Point3D(0, 0, 0)) }

    var currentMoons = moons


    generateSequence(1) { it + 1 }.forEach { step ->
        currentMoons = currentMoons.map { it.applyGravity(currentMoons.minus(it)) }


        if (currentMoons.map { it.velocity }.all { it == ZeroVelocity }) {
            println("Zero velocity at $step")
        }
    }
}
