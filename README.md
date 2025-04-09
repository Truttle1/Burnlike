# Burnlike

This is a cellular automaton made as an attempt to reverse engineer the [Burn](https://esolangs.org/wiki/Burn) cellular automaton. Burn first appeared on the internet in 2008 with no details on its behavior and only an example program: a Rule 110 interpreter. Its creator added more information in 2010 and 2021, but other than that, the language is unimplemented.

I also put something [here](https://esolangs.org/wiki/Talk:Burn#A_ruleset_that_interprets_Rule_110_given_the_example_program) that describes it somewhat more in depth.

Burnlike is a cellular automaton designed to implement Rule 110 given the example program. It has the following rules:

The program tiles repeatedly in all directions. Theoretically it can tile infinitely, but in this interpreter it tiles to a fixed size.

Then, for each generation

* If the difference between a cell channel and its neighbors between the current and previous generation is 1, then that channel decrements by 1. If that goes below the lowest channel value of its neighborhood, it is capped at the lowest.
* If the difference between a cell channel and its neighbors between the current and previous generation is 2, then all channels in the cell decrement by 2. If that goes below the lowest channel value of its neighborhood, it is capped at the lowest.
* If there is a cell above another cell, and the upper cell has a channel with a value of 3 or greater, the lower cell does not decrement.

These rules cause Rule 110 to emerge when the `01` cell is set to `00` on the top row of one of the tiling code patches.

End states for code patches that receive signal from the top (`00` comes in), which represent `1`s in Rule 110, are highlighted in yellow to make the Rule 110 interpretation easier to see.

## Usage

```python burnlike.py rule110.burn```

There are also constants that can be set directly in the Python file for now, perhaps those will be command line args later.

## Controls

**Space**: Run 1 Generation

**Left Shift**: Toggle running generations continuously

**Left Alt**: Cycle numbers on cells between literal values, neighborhood difference change between generations, neighborhood difference, and none

**Click**: *If this is enabled in the code*, adds this code patch to the list of good ones that are highlighted.