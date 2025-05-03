import logging
from typing import List, Dict, Optional
from collections import defaultdict
from dataclasses import dataclass
from flame_calculator import FlameCalculator
from bonus_type import BonusType

# Configuração do logger
logging.basicConfig(
    filename="flame_solver_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("flame_solver")


@dataclass
class FlameLine:
    """
    Represents a single flame bonus line with type, affected stats, tier and value.
    """
    line_type: str
    affected_stats: List[str]
    tier: int
    description: str
    tier_value: int

    @property
    def value(self) -> int:
        return self.tier_value * self.tier

    def __repr__(self) -> str:
        return f"{self.line_type}({self.description}, {self.value}, Tier {self.tier})"


class GlobalFlameSolver:
    """
    Responsible for solving valid flame combinations to meet target stats.
    """

    TOTAL_SLOTS = 4  # Maximum number of flame lines in a combination

    def __init__(self, equip_level: int, debug: bool = True):
        self.equip_level = equip_level
        self.calculator = FlameCalculator()
        self.target_stats: Dict[str, int] = {}
        self.debug = debug

    def _generate_lines(self, tier_min: int = 1, tier_max: int = 7) -> Dict[str, List[FlameLine]]:
        """
        Generate possible flame lines for individual and double stats.
        """
        lines_by_group: Dict[str, List[FlameLine]] = {}

        double_combinations = [
            ("STR", "DEX"), ("STR", "LUK"), ("STR", "INT"),
            ("DEX", "LUK"), ("DEX", "INT"), ("LUK", "INT")
        ]

        # Generate double stat lines
        for stat_a, stat_b in double_combinations:
            if (self.target_stats.get(stat_a, 0) == 0) or (self.target_stats.get(stat_b, 0) == 0):
                continue

            base_value = self.calculator.providers[BonusType.DOUBLE][0].get_base(self.equip_level)
            key = f"Double:{stat_a}+{stat_b}"
            lines_by_group[key] = [
                FlameLine("Double", [stat_a, stat_b], tier, f"{stat_a} + {stat_b}", base_value)
                for tier in range(tier_max, tier_min - 1, -1)
            ]

        # Generate individual stat lines
        for stat in ["STR", "DEX", "INT", "LUK"]:
            if self.target_stats.get(stat, 0) == 0:
                continue

            base_value = self.calculator.providers[BonusType.INDIVIDUAL][0].get_base(self.equip_level)
            key = f"Single:{stat}"
            lines_by_group[key] = [
                FlameLine("Single", [stat], tier, stat, base_value)
                for tier in range(tier_max, tier_min - 1, -1)
            ]

        if self.debug:
            logger.debug("=== GENERATED LINE GROUPS ===")
            for key, group in lines_by_group.items():
                for line in group:
                    logger.debug(line)

        return lines_by_group

    def solve(self, target_stats: Dict[str, int]) -> Optional[List[List[FlameLine]]]:
        """
        Solves for valid flame combinations based on provided target stats.

        Returns:
            List of valid flame combinations or None if no valid combinations exist.
        """
        self.target_stats = target_stats

        tier_groups = [(4, 7), (3, 6), (1, 4)]

        for tier_min, tier_max in tier_groups:
            if self.debug:
                logger.debug(f"\n=== Trying tier group {tier_min}-{tier_max} ===")

            fixed_lines: List[FlameLine] = []
            current_totals: Dict[str, int] = {}

            # Generate fixed lines for guaranteed stats
            for stat in ["ATT", "MATT", "HP", "MP", "ALL_STAT", "DEF", "SPEED", "JUMP", "REQ_LVL"]:
                target_value = target_stats.get(stat, 0)
                if target_value != 0:
                    tier_info = self.calculator.get_tier(self.equip_level, getattr(BonusType, stat), target_value)
                    if tier_info["tier"] is None:
                        print(stat)
                        break  # Impossible to achieve target for this stat

                    fixed_lines.append(FlameLine(stat, [stat], tier_info["tier"], stat, tier_info["value"]))
                    current_totals[stat] = target_value
                else:
                    current_totals[stat] = 0

            if len(fixed_lines) > self.TOTAL_SLOTS:
                continue  # Too many fixed lines for available slots

            flexible_slots = self.TOTAL_SLOTS - len(fixed_lines)
            line_groups = self._generate_lines(tier_min, tier_max)
            group_keys = list(line_groups.keys())
            solutions: List[List[FlameLine]] = []

            def recurse(path: List[FlameLine], totals: Dict[str, int]):
                if solutions:
                    return  # Solution already found

                if len(path) == flexible_slots:
                    # Check if totals match target
                    if all(totals.get(stat, 0) == target for stat, target in target_stats.items()):
                        if self.debug:
                            logger.debug("=== FOUND VALID SOLUTION ===")
                            for line in path:
                                logger.debug(line)

                        solutions.append(fixed_lines + path.copy())
                    return

                for key in group_keys:
                    for line in line_groups[key]:
                        # Skip duplicate lines
                        if any(p.description == line.description and p.line_type == line.line_type for p in path):
                            continue

                        # Check if adding this line exceeds target
                        exceeded = False
                        for stat in line.affected_stats:
                            new_total = totals.get(stat, 0) + line.value
                            target_value = target_stats.get(stat, 0)

                            if target_value > 0 and new_total > target_value:
                                remaining_slots = flexible_slots - len(path) - 1
                                max_possible = remaining_slots * line.value

                                if new_total - target_value > max_possible:
                                    exceeded = True
                                    break

                        if exceeded:
                            continue

                        # Proceed with this line
                        path.append(line)
                        for stat in line.affected_stats:
                            totals[stat] = totals.get(stat, 0) + line.value

                        recurse(path, totals)

                        if solutions:
                            return

                        # Backtrack
                        removed = path.pop()
                        for stat in removed.affected_stats:
                            totals[stat] -= removed.value

            recurse([], current_totals.copy())

            if solutions:
                return solutions

        return None
