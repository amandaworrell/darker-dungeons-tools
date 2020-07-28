"""
Simple API for rolling new characters
"""

import json
from dataclasses import asdict
from typing import Dict, Any, Tuple

import yaml

from darker_dungeons.character import CharacterStats, CharacterSheet, roll_3d6, StatRoller, suggest_stats
from darker_dungeons.random_tables import RandomTable, RandomTableValue, RandomClassTableValue, flatten_selections


def get_base_headers(content_length: int) -> Dict[str, str]:
    return {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        "Content-Length": str(content_length),
    }


def lambda_init() -> Tuple[RandomTable, RandomTable, RandomTable]:
    backgrounds = yaml.load(open("tables/background.yml"), Loader=yaml.BaseLoader)
    background_table: RandomTable[RandomTableValue] = RandomTable.from_dict(backgrounds, 100)

    classes = yaml.load(open("tables/class.yml"), Loader=yaml.BaseLoader)
    class_table: RandomTable[RandomClassTableValue] = RandomTable.from_dict(classes, 100)

    races = yaml.load(open("tables/race.yml"), Loader=yaml.BaseLoader)
    race_table: RandomTable[RandomTableValue] = RandomTable.from_dict(races, 100)

    return background_table, class_table, race_table


BACKGROUND_TABLE, CLASS_TABLE, RACE_TABLE = lambda_init()


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    character_class = flatten_selections(CLASS_TABLE.choose())

    roller = StatRoller(roll_3d6)
    rolled_stats = CharacterStats.roll_stats(roller)
    reroll = roller.roll_stat()
    suggested_stats = suggest_stats(character_class["preferred_stats"], rolled_stats, reroll)

    character = CharacterSheet(
        race=flatten_selections(RACE_TABLE.choose()),
        background=flatten_selections(BACKGROUND_TABLE.choose()),
        character_class=character_class,
        reroll=reroll,
        rolled_stats=rolled_stats,
        suggested_stats=suggested_stats,
    )

    character_dict: Dict[str, Any] = asdict(character)

    character_dict["background"].update({
        "feature": "{{ todo: placeholder }}",
        "family": "{{ todo: placeholder }}",
        "memory": "{{ todo: placeholder }}",
        "motivation": "{{ todo: placeholder }}",
        "habits": "{{ todo: placeholder }}",
        "quest": "{{ todo: placeholder }}",
    })

    character_dict.update({
        "max_hp": "{{ todo: placeholder }}",
        "gold": "{{ todo: placeholder }}",
    })

    character_dict["appearance"] = {
        "age": "{{ todo: placeholder }}",
        "height": "{{ todo: placeholder }}",
        "weight": "{{ todo: placeholder }}",
    }

    character_dict.update({
        "suggested_stats": asdict(character.suggested_stats),
        "rolled_stats": asdict(character.rolled_stats),
        "reroll": character.reroll,
        "attribution": {
            "Random Tables": {
                "author": "Giffyglyph",
                "url": "https://giffyglyph.com/darkerdungeons/",
            },
            "Random Character API": {
                "author": "jworrell",
                "url": "https://github.com/jworrell/darker-dungeons-tools",
            }
        }
    })

    result = json.dumps(character_dict)

    return {
        "statusCode": 200,
        "headers": get_base_headers(len(result)),
        "body": result,
    }


if __name__ == "__main__":
    print(lambda_handler({}, {}))
