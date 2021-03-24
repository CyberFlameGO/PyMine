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
            
"""Contains spawn packets."""

from __future__ import annotations
import uuid

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer


__all__ = (
    "PlayEntitySpawn",
    "PlayLivingEntitySpawn",
    "PlayPaintingSpawn",
    "PlaySpawnExperienceOrb",
    "PlaySpawnPlayer",
    "PlaySpawnPosition",
)


class PlayEntitySpawn(Packet):
    """Sent by the server when a vehicle or other non-living entity is created. Client bound(Server -> Client)."""

    id = 0x00
    to = 1

    def __init__(
        self,
        entity_id: int,
        object_uuid: uuid.UUID,
        type_: int,
        x: int,
        y: int,
        z: int,
        pitch: int,
        yaw: int,
        data: int,
        vloc_x: int,
        vloc_y: int,
        vloc_z: int,
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.object_uuid = object_uuid
        self.type_ = type_
        self.x, self.y, self.z = x, y, z
        self.pitch = pitch
        self.yaw = yaw
        self.data = data
        self.vloc_x = vloc_x
        self.vloc_y = vloc_y
        self.vloc_z = vloc_z

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.object_uuid)
            + Buffer.pack_varint(self.type_)
            + Buffer.pack("d" + self.x)
            + Buffer.pack("d" + self.y)
            + Buffer.pack("d" + self.z)
            + Buffer.pack("i" + self.pitch)
            + Buffer.pack("i" + self.yaw)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_z)
        )


class PlaySpawnExperienceOrb(Packet):
    """Spawns one or more experience orbs. Client bound(Server -> Client)."""

    id = 0x01
    to = 1

    def __init__(self, entity_id: int, x: int = 0, y: int = 0, z: int = 0, count: int = 1237) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.x, self.y, self.z = x, y, z
        self.count = count

    def encode(self):
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("h", self.count)
        )


class PlayLivingEntitySpawn(Packet):
    """Sent by the server when a living entity is spawned.  Client bound(Server -> Client)."""

    id = 0x02
    to = 1

    def __init__(
        self,
        entity_id: int,
        object_uuid: uuid.UUID,
        type_: int,
        x: int,
        y: int,
        z: int,
        pitch: int,
        head_pitch: int,
        yaw: int,
        vloc_x: int,
        vloc_y: int,
        vloc_z: int,
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.object_uuid = object_uuid
        self.type_ = type_
        self.x, self.y, self.z = x, y, z
        self.pitch = pitch
        self.yaw = yaw
        self.head_pitch = head_pitch
        self.vloc_x = vloc_x
        self.vloc_y = vloc_y
        self.vloc_z = vloc_z

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.object_uuid)
            + Buffer.pack_varint(self.type_)
            + Buffer.pack("d" + self.x)
            + Buffer.pack("d" + self.y)
            + Buffer.pack("d" + self.z)
            + Buffer.pack("i" + self.pitch)
            + Buffer.pack("i" + self.yaw)
            + Buffer.pack("i", self.head_pitch)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_z)
        )


class PlayPaintingSpawn(Packet):
    """This packet shows location, name, and type of painting.  Client bound(Server -> Client)."""

    id = 0x03
    to = 1

    def __init__(self, entity_id: int, entity_uuid: uuid.UUID, motive: int, location: int, direction: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.entity_uuid = entity_uuid
        self.motive = motive
        self.location = location
        self.direction = direction

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.entity_uuid)
            + Buffer.pack_varint(self.motive)
            + Buffer.pack_position(self.location)
            + Buffer.pack("b", self.direction)
        )


class PlaySpawnPlayer(Packet):
    """This packet is sent by the server when a player comes into visible range, not when a player joins.
    Clientbound(Server -> Client)"""

    id = 0x04
    to = 1

    def __init__(self, entity_id: int, player_uuid: uuid.UUID, x: int, y: int, z: int, pitch: int, yaw: int) -> None:
        super.__init__()

        self.entity_id = entity_id
        self.player_uuid = player_uuid
        self.x, self.y, self.z = x, y, z
        self.pitch, self.yaw = pitch, yaw

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.player_uuid)
            + Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("B", self.pitch)
            + Buffer.pack("B", self.yaw)
        )


class PlaySpawnPosition(Packet):
    """insert fancy docstring here (server -> client)"""

    id = 0x42
    to = 1

    def __init__(self, x: int, y: int, z: int) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z

    def encode(self) -> bytes:
        return Buffer.pack_position(self.x, self.y, self.z)
