from enum import Enum

class BonusType(Enum):
    INDIVIDUAL = "individual"   # Single stats (STR, DEX, INT, LUK)
    DOUBLE = "double"           # Double stat bonuses (e.g., STR + DEX)
    ATT = "att"                 # Attack bonus
    MATT = "matt"               # Magic attack bonus
    HP = "hp"                   # HP bonus
    MP = "mp"                   # MP bonus
    ALL_STAT = "all_stat"       # All stats bonus
    DEF = "def"                 # Defense bonus
    SPEED = "speed"             # Speed bonus
    JUMP = "jump"               # Jump bonus
    REQ_LVL = "req_lvl"         # Required level reduction
