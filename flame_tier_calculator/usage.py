"""
Example script to execute the GlobalFlameSolver and display formatted results.
"""

import time
from collections import defaultdict
from typing import Dict
from global_flame_solver import GlobalFlameSolver

start_time = time.time()

# Example request configuration
request: Dict = {
    "equip_level": 200,
    "stats": {
        "STR": 66,
        "DEX": 0,
        "INT": 0,
        "LUK": 0,
        "ATT": 0,
        "MATT": 0,
        "HP": 0,
        "MP": 0,
        "ALL_STAT": 5,
        "DEF": 66,
        "SPEED": 0,
        "JUMP": 0,
        "REQ_LVL": -25
    }
}

# Initialize solver and solve
solver = GlobalFlameSolver(equip_level=request["equip_level"])
solutions = solver.solve(request["stats"])


if not solutions:
    print("No valid combination found.")
else:
    target_stats = request["stats"]

    for solution in solutions:
        result_data = []

        # Process solution lines
        for line in solution:
            if line.line_type in ["ATT", "MATT", "HP", "MP", "ALL_STAT", "DEF", "SPEED", "JUMP", "REQ_LVL"]:
                result_data.append((line.description, request["stats"][line.description], line.tier, "FIXED"))
            elif line.line_type == "Double":
                result_data.append((" + ".join(line.affected_stats), line.value, line.tier, "DOUBLE"))
            else:
                result_data.append((line.description, line.value, line.tier, "SINGLE"))

        # Group results
        grouped = defaultdict(lambda: [0, 0, ""])
        for stat, value, tier, line_type in result_data:
            grouped[stat][0] += value
            grouped[stat][1] = tier
            grouped[stat][2] = line_type

        # Print coverage summary
        print("\n------- Coverage Summary -------")
        print(f"{'Stat':<12} | {'Target':<7} | {'Total Found':<11}")
        print("-" * 37)

        real_totals = defaultdict(int)

        for stat, (quantity, tier, line_type) in grouped.items():
            if " + " in stat:
                stat_parts = stat.split(" + ")
                for part in stat_parts:
                    real_totals[part] += quantity
            else:
                real_totals[stat] += quantity

        for stat, target in target_stats.items():
            total_found = real_totals.get(stat, 0)
            print(f"{stat:<12} | {target:<7} | {total_found:<11}")


        # Print result table
        print("\n===========  Result  ===========\n")

        print(f"{'Stat':<12} | {'Quantity':<8} | {'Tier':<4}")
        print("-" * 31)
        for stat, (quantity, tier, _) in grouped.items():
            print(f"{stat:<12} | {quantity:<8} | {tier:<4}")

        elapsed = time.time() - start_time

        print(f"\nExecution time: {elapsed:.3f} seconds.")


