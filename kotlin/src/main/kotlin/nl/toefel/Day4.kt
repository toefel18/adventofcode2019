package nl.toefel

fun main() {
    val (start, max) = listOf(152085, 670283)
    val options = (start..max).map { it.toString() }.filter { hasAdjacentDigits(it) }.filter { onlyIncreasing(it) }
    println("part 1 = ${options.size}")

    val part2Options = (start..max)
        .map { it.toString() }
        .filter { hasAdjacentDigitsNotTakingSequencesLargerThan2IntoAccount(it) }
        .filter { onlyIncreasing(it) }

    println("part 2 = ${part2Options.size}")
}

fun hasAdjacentDigits(pwd: String): Boolean {
    for (i in 1 until pwd.length) {
        if (pwd[i-1] == pwd[i]) return true
    }
    return false
}

fun onlyIncreasing(pwd: String): Boolean {
    for (i in 1 until pwd.length) {
        if (pwd[i-1].toByte() > pwd[i].toByte()) return false
    }
    return true
}

fun hasAdjacentDigitsNotTakingSequencesLargerThan2IntoAccount(pwd: String): Boolean {
    for (i in 1 until (pwd.length - 1)) {
        if (pwd[i-1] == pwd[i] && pwd[i] == pwd[i+1]) {
            // filter sequences longer than 2 and try again
            return hasAdjacentDigitsNotTakingSequencesLargerThan2IntoAccount(pwd.filter { it != pwd[i] })
        }
    }
    // no sequences longer than 3 found, now check if there is a group
    return hasAdjacentDigits(pwd)
}
