
# MapleStory Flame Solver

This project aims to calculate and simulate possible combinations of **Bonus Stats (Flames)** on equipment in **MapleStory**, based on defined rules for each type of bonus and equipment level.

It is a useful tool for players and developers who want to predict, analyze, or create strategies to optimize Flames on equipment in the game.

## Data Source

The base data (minimum and maximum values per equipment level and stat type) was extracted from the following community official page:

[MapleStory Bonus Stats - StrategyWiki](https://strategywiki.org/wiki/MapleStory/Bonus_Stats)

These values were organized in `base_values.py` tables to allow fast and flexible calculations in the algorithm.

## Project Goals

- Simulate Flames on equipment based on MapleStory's tier and stat value rules.
- Find possible combinations to reach desired target stats.
- Enable analysis and testing for equipment optimization planning.

## Project Structure

```
.
├── base_values.py          # Base tables for level and stat values
├── bonus_type.py          # Enum for available bonus types
├── flame_analyzer.py      # Simplified interface for finding valid Flames
├── flame_calculator.py    # Core logic for tier calculation and value lookup
├── global_flame_solver.py # Solver to find valid combinations for target stats
├── stat_calculator.py     # Tier calculation logic
├── usage.py               # Example usage script with formatted output
```

## How to Use

Install required packages (`numba` is required):

```bash
pip install numba
```

Run the example:

```bash
python usage.py
```

You will see an example simulation like this:

```
------- Coverage Summary -------
Stat         | Target  | Total Found
-------------------------------------
STR          | 66      | 66
ALL_STAT     | 5       | 5
DEF          | 66      | 66
REQ_LVL      | -25     | -25

===========  Result  ===========

Stat         | Quantity | Tier
-----------------------------------
STR          | 66       | 6
ALL_STAT     | 5        | 5
DEF          | 66       | 6
REQ_LVL      | -25      | 5

Execution time: 0.150 seconds.
```

## Features

- **Quick analysis**: Precomputed data for fast tier and value lookups.
- **Smart solver**: Algorithm to find possible combinations with optimized search.
- **Modular**: Separated modules for clean and reusable logic.

## Notes

- This project does not connect to the actual game, it is a simulation based on official game rules.
- Always refer to the official source if the game receives updates.

## License

This project is free to use for study and personal usage.

## Credits

- [MapleStory Bonus Stats - StrategyWiki](https://strategywiki.org/wiki/MapleStory/Bonus_Stats) for providing detailed rules on Flames.
- MapleStory community for sharing knowledge and making this kind of tool possible.
