from numba import njit
from typing import Tuple

@njit
def calculate_tier(base: int, stat_value: int, formula_mode: int) -> Tuple[int, int]:
    """
    Calculate the tier based on base value, target stat value and formula mode.

    Args:
        base (int): Base value depending on the equipment level.
        stat_value (int): The desired stat value to achieve.
        formula_mode (int): Calculation mode. 
                            0 = value = base * tier
                            1 = value = tier directly

    Returns:
        Tuple[int, int]: (tier, value) if stat_value matches; otherwise (-1, -1).
    """
    for tier in range(1, 8):
        if formula_mode == 0:
            value = base * tier
        elif formula_mode == 1:
            value = tier
        else:
            raise ValueError("Invalid formula mode")

        if value == stat_value:
            return tier, value

    return -1, -1
