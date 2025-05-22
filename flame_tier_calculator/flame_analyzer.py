from typing import Dict, List, Any
from flame_tier_calculator.global_flame_solver import GlobalFlameSolver

class FlameAnalyzer:
    """
    Simplified interface to analyze flame combinations based on target stats.
    """

    def __init__(self, equip_level: int):
        """
        Initialize the analyzer with the equipment level.

        Args:
            equip_level (int): The equipment level to use for calculations.
        """
        self.equip_level = equip_level

    def analyze(self, stats: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Analyzes the target stats and returns possible flame solutions.

        Args:
            stats (Dict[str, int]): Target stats to solve for.

        Returns:
            List[Dict[str, Any]]: A list of flame line details or an error message.
        """
        solver = GlobalFlameSolver(self.equip_level)
        solutions = solver.solve(stats)

        if not solutions:
            return [{"error": "No valid flame combinations found."}]

        formatted_solutions = [
            {
                "type": line.line_type,
                "stat": line.description,
                "tier": line.tier,
                "value": line.value
            }
            for line in solutions[0]
        ]

        return formatted_solutions
