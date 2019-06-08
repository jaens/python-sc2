#!/usr/bin/env python3

from typing import List, Tuple, Any

from s2clientprotocol import common_pb2 as common_pb
from s2clientprotocol import data_pb2 as data_pb
from s2clientprotocol import error_pb2 as error_pb
from s2clientprotocol import raw_pb2 as raw_pb
from s2clientprotocol import sc2api_pb2 as sc_pb

ENUMS: List[Tuple[str, List[Tuple[str, Any]]]] = [
    ("CreateGameError", sc_pb.ResponseCreateGame.Error.items()),
    ("PlayerType", sc_pb.PlayerType.items()),
    ("Difficulty", sc_pb.Difficulty.items()),
    ("AIBuild", sc_pb.AIBuild.items()),
    ("Status", sc_pb.Status.items()),
    ("Result", sc_pb.Result.items()),
    ("Alert", sc_pb.Alert.items()),
    ("ChatChannel", sc_pb.ActionChat.Channel.items()),
    ("Race", common_pb.Race.items()),
    ("DisplayType", raw_pb.DisplayType.items()),
    ("Alliance", raw_pb.Alliance.items()),
    ("CloakState", raw_pb.CloakState.items()),
    ("Attribute", data_pb.Attribute.items()),
    ("TargetType", data_pb.Weapon.TargetType.items()),
    ("Target", data_pb.AbilityData.Target.items()),
    ("ActionResult", error_pb.ActionResult.items()),
]

header = """
from enum import Enum
"""

RESERVED = {"None"}

with open('sc2/data_enums.py', 'w') as f:
    def l(s=""):
        print(s, file=f)

    l(header)
    for (name, items) in ENUMS:
        l(f'class {name}(Enum):')
        for key, value in items:
            if key in RESERVED:
                continue
            l(f'    {key} = {value !r}')
        l()
