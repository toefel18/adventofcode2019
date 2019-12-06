package nl.toefel

import java.io.File

fun main() {
    val edges = File(ClassLoader.getSystemResource("day6-input.txt").file)
        .readLines()
        .map { it.split(")")[1] to it.split(")")[0] }
        .toMap()

    val vertices = (edges.keys + edges.values).toSet().minus("COM")
    val orbits = vertices.map { countOrbits(from = it, to = "COM", edges = edges) }.sum()
    println("part1 = $orbits")

    val sanOrbiting = orbitPath(from = "SAN", to = "COM", edges = edges).reversed()
    val youOrbiting = orbitPath(from = "YOU", to = "COM", edges = edges).reversed()
    val pathsJoinAtObject = youOrbiting.find { sanOrbiting.indexOf(it) > 0 }
    val stepsBetween = sanOrbiting.indexOf(pathsJoinAtObject) + youOrbiting.indexOf(pathsJoinAtObject)
    println("part2 = $stepsBetween")
}

fun countOrbits(from: String, to: String, edges: Map<String, String>): Long =
    if (edges[from] == to) 1 else 1 + countOrbits(edges[from]!!, to, edges)

fun orbitPath(from: String, to: String, edges: Map<String, String>): List<String> {
    val next = edges[from]
    return if (next == to) return listOf(next) else orbitPath(next!!, to, edges) + next
}