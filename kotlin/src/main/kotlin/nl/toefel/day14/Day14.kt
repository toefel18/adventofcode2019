package nl.toefel.day14

import java.io.File

// helper classes to transform input
data class InputChemicalAmount(val chemicalName: String, val amount: Int)
data class InputReaction(val chemicalName: String, val batchSize: Int, val ingredients: List<InputChemicalAmount>)


data class Chemical(val name: String, val batchSize: Int, val ingredients: List<ChemicalIngredient>, var requiredAmountForFuel: Long = 0, var amountAlreadyProduced: Long = 0) {
    fun addRequiredAmount(amount: Long) {
        val newRequiredAmountForFuel = requiredAmountForFuel + amount
        requiredAmountForFuel = newRequiredAmountForFuel

        if (amountAlreadyProduced < newRequiredAmountForFuel) {
            val newAmountAlreadyProduced = scaleToNextMultipleOfBatchSize(newRequiredAmountForFuel)
            val amountToPassDown = (newAmountAlreadyProduced - amountAlreadyProduced) / batchSize
            ingredients.forEach { ingredient -> ingredient.chemical.addRequiredAmount(ingredient.amount * amountToPassDown) }
            amountAlreadyProduced = newAmountAlreadyProduced
        }
    }

    private fun scaleToNextMultipleOfBatchSize(newRequirement: Long): Long {
        val remainder = newRequirement % batchSize
        return if (remainder == 0L) { newRequirement } else { newRequirement + (batchSize - remainder) }
    }
}

data class ChemicalIngredient(val amount: Int, val chemical: Chemical)

// can be applied multiple times per line to read a number and chemical name.
val amountAndChemicalRegex = "([0-9]+) ([a-zA-Z]+)".toRegex()

fun main() {
    val reactions = File(ClassLoader.getSystemResource("day14-input.txt").file).readLines()
        .map { extractChemicalAmounts(it) }
        .map { InputReaction(it.last().chemicalName, it.last().amount, it.dropLast(1)) }

    val fuelReactionGraph = buildGraph("FUEL", reactions)

    // calculate requirements for 1 FUEL
    fuelReactionGraph.getValue("FUEL").addRequiredAmount(1)
    println("Part 1, total produced: " + fuelReactionGraph.getValue("ORE").amountAlreadyProduced)

    binarySearchFuelValueThatRequiresTrillionOre(reactions)
}

fun buildGraph(startChemical: String, reactions: List<InputReaction>): MutableMap<String, Chemical> {
    val reactionByName = reactions.associateBy { it.chemicalName }

    // keeps track of all vertices in the graph, ORE is the leaf, add it already
    val graphVerticesByName = mutableMapOf("ORE" to Chemical("ORE", 1, listOf()))

    fun build(chemicalName: String): Chemical {
        val reaction = reactionByName.getValue(chemicalName)

        val ingredients = reaction.ingredients.map {
            val ingredient = graphVerticesByName[it.chemicalName] ?: build(it.chemicalName)
            ChemicalIngredient(it.amount, ingredient)
        }

        val reactionGraphVertex = Chemical(reaction.chemicalName, reaction.batchSize, ingredients)
        graphVerticesByName[reactionGraphVertex.name] = reactionGraphVertex
        return reactionGraphVertex
    }

    build(startChemical)
    return graphVerticesByName
}

fun binarySearchFuelValueThatRequiresTrillionOre(reactions: List<InputReaction>) {
    val targetAmountOre = 1000000000000L
    var fuelAmountRangeStart = 0
    var fuelAmountRangeEnd = 50000000

    while (true) {
        // select middle of range
        val currentFuelValue = fuelAmountRangeStart + ((fuelAmountRangeEnd - fuelAmountRangeStart) / 2)

        // calculate required ore
        val fuelReactionGraph = buildGraph("FUEL", reactions)
        fuelReactionGraph.getValue("FUEL").addRequiredAmount(currentFuelValue.toLong())
        val oreRequiredForFuel = fuelReactionGraph.getValue("ORE").amountAlreadyProduced

        // check if we have an (approximate) result
        println("fuel=${currentFuelValue}  ore required = $oreRequiredForFuel")
        if (fuelAmountRangeEnd - fuelAmountRangeStart  < 2) {
            println("Closest guess = $currentFuelValue")
            break;
        } else if (oreRequiredForFuel < targetAmountOre) {
            fuelAmountRangeStart = currentFuelValue
        } else if (oreRequiredForFuel > targetAmountOre) {
            fuelAmountRangeEnd = currentFuelValue
        } else {
            println("Found result = $currentFuelValue")
            break;
        }
    }
}

private fun extractChemicalAmounts(it: String) =
    amountAndChemicalRegex.findAll(it).toList().map { matchResult -> InputChemicalAmount(matchResult.groupValues[2], matchResult.groupValues[1].toInt()) }
