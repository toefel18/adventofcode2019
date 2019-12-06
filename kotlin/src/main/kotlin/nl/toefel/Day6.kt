package nl.toefel

import java.io.File

fun main() {
    val edges = File(ClassLoader.getSystemResource("day6-input.txt").file)
        .readLines()
        .map { it.split(")")[1] to it.split(")")[0] }
        .toMap()

    val vertices = (edges.keys + edges.values).toSet().minus("COM")
    val orbits = vertices.map { countOrbitsTo(it, "COM", edges) }.sum()
    println("part1 = $orbits")
}

fun countOrbitsTo(from: String, to: String, edges: Map<String, String>): Long {
    val next = edges[from]
    return if (next == to) return 1 else 1 + countOrbitsTo(next!!, to, edges)
}
