from __future__ import annotations

from typing import Optional, Union, Tuple

from . import unit as unit_module
from .ids.ability_id import AbilityId
from .position import Point2


class UnitCommand:
    def __init__(self, ability: AbilityId, unit: unit_module.Unit, target: Optional[Union[Point2, unit_module.Unit]]=None, queue=False):
        assert ability in AbilityId, f"ability {ability} is not in AbilityId"
        assert isinstance(unit, unit_module.Unit), f"unit {unit} is of type {type(unit)}"
        assert target is None or isinstance(
            target, (Point2, unit_module.Unit)
        ), f"target {target} is of type {type(target)}"
        assert isinstance(queue, bool), f"queue flag {queue} is of type {type(queue)}"
        self.ability = ability
        self.unit = unit
        self.target = target
        self.queue = queue

    @property
    def combining_tuple(self) -> Tuple[AbilityId, Optional[Union[Point2, unit_module.Unit]], bool]:
        return (self.ability, self.target, self.queue)

    def __repr__(self):
        return f"UnitCommand({self.ability}, {self.unit}, {self.target}, {self.queue})"
