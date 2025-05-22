import time
from collections import defaultdict
from typing import Dict, Optional, Any
from flame_tier_calculator.global_flame_solver import GlobalFlameSolver

class FlameValues:
    def __init__(
        self,
        equip_level: int = 0,
        STR: int = 0,
        DEX: int = 0,
        INT: int = 0,
        LUK: int = 0,
        ATT: int = 0,
        MATT: int = 0,
        HP: int = 0,
        MP: int = 0,
        ALL_STAT: int = 0,
        DEF: int = 0,
        SPEED: int = 0,
        JUMP: int = 0,
        REQ_LVL: int = 0
    ):
        self.equip_level = equip_level
        self.stats = {
            "STR": STR,
            "DEX": DEX,
            "INT": INT,
            "LUK": LUK,
            "ATT": ATT,
            "MATT": MATT,
            "HP": HP,
            "MP": MP,
            "ALL_STAT": ALL_STAT,
            "DEF": DEF,
            "SPEED": SPEED,
            "JUMP": JUMP,
            "REQ_LVL": REQ_LVL,
        }

    def run(self) -> Dict[str, Any]:
        start_time = time.time()
        solver = GlobalFlameSolver(equip_level=self.equip_level)
        solutions = solver.solve(self.stats)

        if not solutions:
            return {
                "error": "No valid combination found.",
                "execution_time": time.time() - start_time,
            }

        results = []
        for solution in solutions:
            result_data = []

            for line in solution:
                if line.line_type in ["ATT", "MATT", "HP", "MP", "ALL_STAT", "DEF", "SPEED", "JUMP", "REQ_LVL"]:
                    result_data.append({
                        "stat": line.description,
                        "value": self.stats.get(line.description, 0),
                        "tier": line.tier,
                        "type": "FIXED"
                    })
                elif line.line_type == "Double":
                    result_data.append({
                        "stat": " + ".join(line.affected_stats),
                        "value": line.value,
                        "tier": line.tier,
                        "type": "DOUBLE"
                    })
                else:
                    result_data.append({
                        "stat": line.description,
                        "value": line.value,
                        "tier": line.tier,
                        "type": "SINGLE"
                    })

            # Agrupa resultados para sumarizar
            grouped = defaultdict(lambda: {"total_value": 0, "tier": 0, "type": ""})
            for entry in result_data:
                stat = entry["stat"]
                grouped[stat]["total_value"] += entry["value"]
                grouped[stat]["tier"] = entry["tier"]
                grouped[stat]["type"] = entry["type"]

            # Calcula totais por estatística (considerando combos "A + B")
            real_totals = defaultdict(int)
            for stat, info in grouped.items():
                if " + " in stat:
                    parts = stat.split(" + ")
                    for part in parts:
                        real_totals[part] += info["total_value"]
                else:
                    real_totals[stat] += info["total_value"]

            execution_time = time.time() - start_time

            results.append({
                "lines": result_data,
                "summary": grouped,
                "totals": real_totals,
                "execution_time": execution_time,
            })

        return {"solutions": results}
