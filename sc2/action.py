from __future__ import annotations

from itertools import groupby
from typing import Iterable, Iterator, TYPE_CHECKING

from s2clientprotocol import common_pb2 as common_pb
from s2clientprotocol import raw_pb2 as raw_pb

from .position import Point2
from .unit import Unit

if TYPE_CHECKING:
    from .unit_command import UnitCommand

def combine_actions(action_iter: Iterable[UnitCommand]) -> Iterator[raw_pb.ActionRaw]:
    for key, items in groupby(action_iter, key=lambda a: a.combining_tuple):
        ability, target, queue = key

        if target is None:
            cmd = raw_pb.ActionRawUnitCommand(
                ability_id=ability.value,
                unit_tags=list({u.unit.tag for u in items}),
                queue_command=queue
            )
        elif isinstance(target, Point2):
            cmd = raw_pb.ActionRawUnitCommand(
                ability_id=ability.value,
                unit_tags=list({u.unit.tag for u in items}),
                queue_command=queue,
                target_world_space_pos=common_pb.Point2D(x=target.x, y=target.y),
            )
        elif isinstance(target, Unit):
            cmd = raw_pb.ActionRawUnitCommand(
                ability_id=ability.value,
                unit_tags=[u.unit.tag for u in items],
                queue_command=queue,
                target_unit_tag=target.tag,
            )
        else:
            raise RuntimeError(f"Must target a unit, point or None, found '{target !r}'")

        yield raw_pb.ActionRaw(unit_command=cmd)
