"""
Provides logic to calculate flame tiers and values based on equipment level and bonus types.
"""

from flame_tier_calculator.bonus_type import BonusType
from flame_tier_calculator.base_values import INDIVIDUAL_BASE_BY_LEVEL, DOUBLE_BASE_BY_LEVEL, HP_MP_BASE_BY_LEVEL, DEF_BASE_BY_LEVEL
from flame_tier_calculator.stat_calculator import calculate_tier
import bisect
from typing import Union, Tuple, Callable, Dict

class BaseValueProvider:
    """
    Provides base stat values according to the equipment level using lookup tables.
    """

    def __init__(self, level_table: list):
        self.levels = [row[0] for row in level_table]
        self.bases = [row[2] for row in level_table]

    def get_base(self, level: int) -> int:
        """
        Returns the base value corresponding to the equipment level.
        """
        index = bisect.bisect_right(self.levels, level) - 1
        return self.bases[index]


class FlameCalculator:
    """
    Determines tier and calculated stat values based on bonus type and equipment level.
    """

    def __init__(self):
        self.providers: Dict[BonusType, Tuple[Union[BaseValueProvider, Callable[[int], int]], int]] = {
            BonusType.INDIVIDUAL: (BaseValueProvider(INDIVIDUAL_BASE_BY_LEVEL), 0),
            BonusType.DOUBLE: (BaseValueProvider(DOUBLE_BASE_BY_LEVEL), 0),
            BonusType.HP: (BaseValueProvider(HP_MP_BASE_BY_LEVEL), 0),
            BonusType.MP: (BaseValueProvider(HP_MP_BASE_BY_LEVEL), 0),
            BonusType.ATT: (lambda lvl: 1, 1),
            BonusType.MATT: (lambda lvl: 1, 1),
            BonusType.ALL_STAT: (lambda lvl: 1, 1),
            BonusType.DEF: (BaseValueProvider(DEF_BASE_BY_LEVEL), 0),
            BonusType.SPEED: (lambda lvl: 1, 1),
            BonusType.JUMP: (lambda lvl: 1, 1),
            BonusType.REQ_LVL: (lambda lvl: -5, 0),

        }

    def get_tier(self, equip_level: int, bonus_type: BonusType, stat_value: int) -> Dict[str, Union[int, None]]:
        """
        Calculates the tier for the given stat value based on bonus type and equipment level.
        """
        provider, formula_mode = self.providers.get(bonus_type)

        base = provider(equip_level) if callable(provider) else provider.get_base(equip_level)

        tier, calculated_value = calculate_tier(base, stat_value, formula_mode)

        if tier == -1:
            return {"tier": None, "value": None}

        return {"tier": tier, "value": calculated_value}
