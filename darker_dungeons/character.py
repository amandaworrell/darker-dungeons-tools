import random
from dataclasses import dataclass, asdict
from typing import Optional, Mapping, Callable, List


def roll_3d6() -> int:
    return sum(random.randint(1, 6) for _ in range(3))


@dataclass
class StatRoller:
    _roll_stat: Callable[[], int]

    def roll_stat(self):
        return self._roll_stat()


@dataclass
class CharacterStats:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    @staticmethod
    def roll_stats(roller: StatRoller) -> 'CharacterStats':
        return CharacterStats(
            strength=roller.roll_stat(),
            dexterity=roller.roll_stat(),
            constitution=roller.roll_stat(),
            intelligence=roller.roll_stat(),
            wisdom=roller.roll_stat(),
            charisma=roller.roll_stat(),
        )


def suggest_stats(preferred_stats: List[str], rolled_stats: CharacterStats, reroll: int):
    rolled_stats_dict = asdict(rolled_stats)

    worst_stat = min((v, k) for k, v in rolled_stats_dict.items())

    if worst_stat[0] < reroll:
        rolled_stats_dict[worst_stat[1]] = reroll

    _ = max((v, k) for k, v in rolled_stats_dict.items())

    return CharacterStats(**rolled_stats_dict)


@dataclass
class CharacterSheet:
    race: Mapping[str, str]
    background: Mapping[str, str]
    character_class: Mapping[str, str]
    reroll: int
    rolled_stats: CharacterStats
    suggested_stats: Optional[CharacterStats]
