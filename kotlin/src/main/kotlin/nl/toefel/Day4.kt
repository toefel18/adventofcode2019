package nl.toefel

fun main() {
    val range = (152085..670283).map { it.toString() }.filter { onlyIncreasing(it) }

    val options = range.filter { hasAdjacentDigits(it) }
    println("part 1 = ${options.size}")

    val part2Options = range.filter { hasSinglePairOfAdjacentDigits(it) }
    println("part 2 = ${part2Options.size}")
}

fun hasAdjacentDigits(pwd: String) = (1 until pwd.length).any { pwd[it - 1] == pwd[it] }
fun onlyIncreasing(pwd: String) = (1 until pwd.length).all { pwd[it - 1].toInt() <= pwd[it].toInt() }

fun hasSinglePairOfAdjacentDigits(pwd: String): Boolean {
    for (i in 1 until (pwd.length - 1)) {
        if (pwd[i - 1] == pwd[i] && pwd[i] == pwd[i + 1]) {
            // filter sequences longer than 2 and try again
            return hasSinglePairOfAdjacentDigits(pwd.filter { it != pwd[i] })
        }
    }
    // no sequences longer than 3 found, now check if there is a group
    return hasAdjacentDigits(pwd)
}
