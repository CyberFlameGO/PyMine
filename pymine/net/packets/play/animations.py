# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Contains animation packets."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayEntityAnimation",
    "PlayBlockBreakAnimation",
    "PlayAnimationServerBound",
    "PlayOpenBook",
)


class PlayEntityAnimation(Packet):
    """Sent whenever an entity should change animation. (Server -> Client)

    :param int entity_id: Entity ID of the digging entity.
    :param int animation: Value 0-5 which correspond to a specific animation (https://wiki.vg/Protocol#Entity_Animation_.28clientbound.29).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar animation:
    """

    id = 0x05
    to = 1

    def __init__(self, entity_id: int, animation: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.animation = animation

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack("B", self.animation)


class PlayBlockBreakAnimation(Packet):
    """Sent to play a block breaking animation. (Server -> Client)

    :param int entity_id: Entity ID of the entity which broke the block, or random.
    :param int x: The x coordinate of the location to play the animation.
    :param int y: The y coordinate of the location to play the animation.
    :param int z: The z coordinate of the location to play the animation.
    :param int stage: Stage from 0-9 in the breaking animation.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar stage:
    """

    id = 0x08
    to = 1

    def __init__(self, entity_id: int, x: int, y: int, z: int, stage: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.x, self.y, self.z = x, y, z
        self.stage = stage

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack_position(self.x, self.y, self.z) + Buffer.pack("b", self.stage)


class PlayAnimationServerBound(Packet):
    """Sent when a client's arm swings. (Client -> Server)

    :param int hand: Either main hand (0) or offhand (1).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar hand:
    """

    id = 0x2C
    to = 0

    def __init__(self, hand: int) -> None:
        super().__init__()

        self.hand = hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayAnimationServerBound:
        return cls(buf.unpack_varint())


class PlayOpenBook(Packet):
    """Sent when a player right clicks a signed book. (Server -> Client)

    :param int hand: The hand used, either main (0) or offhand (1).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar hand:
    """

    id = 0x2C
    to = 1

    def __init__(self, hand: int) -> None:
        super().__init__()

        self.hand = hand

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.hand)
