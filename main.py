from flame_tier_calculator.flame_values import FlameValues

def pretty_print_results(results: dict):
    solutions = results.get('solutions')
    if not solutions:
        print("No solutions found or error:", results.get('error', 'No data'))
        return

    # Use only the first solution
    sol = solutions[0]

    print(f"\nSolution:")
    exec_time = sol.get('execution_time')
    if exec_time is not None:
        print(f"Execution Time: {exec_time:.4f} seconds")

    # Print totals
    print("\nTotals:")
    print(f"{'Stat':<20} | {'Total':>5}")
    print("-" * 28)
    totals = sol.get('totals', {})
    for stat, total in totals.items():
        print(f"{stat:<20} | {total:>5}")

    # Print lines without the 'type' field
    print("\nLines:")
    print(f"{'Stat':<20} | {'Value':>5} | {'Tier':>4}")
    print("-" * 35)
    for line in sol.get('lines', []):
        stat = line.get('stat', 'N/A')
        value = line.get('value', 'N/A')
        tier = line.get('tier', 'N/A')
        print(f"{stat:<20} | {value:>5} | {tier:>4}")

    print("\n" + "-" * 50)


usage = FlameValues(equip_level=250, STR=95, DEX=63, LUK=28, ALL_STAT=6)
result = usage.run()

pretty_print_results(result)
