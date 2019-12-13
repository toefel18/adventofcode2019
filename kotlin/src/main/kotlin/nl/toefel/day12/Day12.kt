package nl.toefel.day12

import java.io.File
import java.lang.Integer.max
import kotlin.math.absoluteValue
import kotlin.math.sign


data class Point3D(val x: Int, val y: Int, val z: Int) {
    fun applyGravity(other: Point3D) = Point3D(
        x = other.x.compareTo(this.x).sign,
        y = other.y.compareTo(this.y).sign,
        z = other.z.compareTo(this.z).sign)

    operator fun plus(other: Point3D) = Point3D(this.x + other.x, this.y + other.y, this.z + other.z)
    fun energy(): Int = x.absoluteValue + y.absoluteValue + z.absoluteValue
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
    part2()
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

private fun part2() {
    val moons = File(ClassLoader.getSystemResource("day12-input.txt").file).readLines()
        .map { it.split(", |<|>|=".toRegex()) }
        .map { Moon(Point3D(it[2].toInt(), it[4].toInt(), it[6].toInt()), Point3D(0, 0, 0)) }

    var currentMoons = moons

    // maps moon.x,y,z to the list of velocities
    // for example:
    // 0.x 1 2 1 2 1 2
    // 0.y 3 4 3 4
    // ..
    // 3.z 9 8 9 8
    val velocityValues = mutableMapOf<String, MutableList<Long>>()

    // initialize first values (all 0)
    currentMoons.writeVelocityTo(velocityValues)

    // find the repeating sequence per moon per velocity
    var periods = velocityValues.findRepeatingSequenceLengths(0)

    // keep computing values until we find a period (repeated sequence) for each moons velocity axis
    generateSequence(1) { it + 1 }.takeWhile { !periods.values.all { it > 0 } }.forEach { step ->
        currentMoons = currentMoons.map { it.applyGravity(currentMoons.minus(it)) }
        currentMoons.writeVelocityTo(velocityValues)
        periods = velocityValues.findRepeatingSequenceLengths(step)
    }

    periods.forEach { (k, v) -> println("$k $v") }

    // now compute the least common multiple of all the sequence lengths
    val leastCommonMultipleOfAllSequences = periods.values.reduce { acc, next -> lcm2(acc, next)}
    println("Least common multiple of all sequences = $leastCommonMultipleOfAllSequences")
}

fun List<Moon>.writeVelocityTo(velocities: MutableMap<String, MutableList<Long>>) {
    forEachIndexed { moonNumber, moon ->
        velocities.computeIfAbsent("$moonNumber.x") { mutableListOf() }.add(moon.velocity.x.toLong())
        velocities.computeIfAbsent("$moonNumber.y") { mutableListOf() }.add(moon.velocity.y.toLong())
        velocities.computeIfAbsent("$moonNumber.z") { mutableListOf() }.add(moon.velocity.z.toLong())
    }
}

val cache: MutableMap<String, Long> = mutableMapOf()

fun MutableMap<String, MutableList<Long>>.findRepeatingSequenceLengths(step: Int): Map<String, Long> {
    return this.mapValues { entry ->
        if (cache.containsKey(entry.key)) {
            cache[entry.key]!!
        } else {
            val sequenceLength = findRepeatingSequence(entry.value, step)
            if (sequenceLength > 0) {
                cache[entry.key] = sequenceLength
            }
            sequenceLength
        }
    }
}

fun findRepeatingSequence(intList: List<Long>, step: Int): Long {
    (max(step / 2 - 1, 0) until intList.size / 2).forEach { idx ->
        val currentPeriod = intList.subList(0, idx)
        val nextPeriod = intList.subList(idx, 2 * idx)
        if (currentPeriod == nextPeriod) {
            return currentPeriod.size.toLong()
        }
    }
    return 0
}

// greatest common divisor
fun gcd(a: Long, b: Long): Long = if (b == 0L) a else gcd(b, a % b)

// a simpler implementation like (a * b) / gcd(a, b) overflows and provides the wrong answer
// taken from https://www.baeldung.com/java-least-common-multiple
fun lcm2(number1: Long, number2: Long): Long {
    if (number1 == 0L || number2 == 0L) {
        return 0
    }
    val absNumber1 = Math.abs(number1)
    val absNumber2 = Math.abs(number2)
    val absHigherNumber = Math.max(absNumber1, absNumber2)
    val absLowerNumber = Math.min(absNumber1, absNumber2)
    var lcm = absHigherNumber
    while (lcm % absLowerNumber != 0L) {
        lcm += absHigherNumber
    }
    return lcm
}