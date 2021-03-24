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
            
"""Contains packets that are related to particles."""
from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayParticle",)


class PlayParticle(Packet):
    """Displays the named particle."""

    id = 0x22
    to = 1

    def __init__(
        self,
        particle_id: int,
        long_distance: bool,
        x: int,
        y: int,
        z: int,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        particle_data: float,
        particle_count: int,
        data: dict,
    ) -> None:
        super().__init__()

        self.part_id = particle_id
        self.long_dist = long_distance
        self.x, self.y, self.z = x, y, z
        self.off_x, self.off_y, self.set_z = offset_x, offset_y, offset_z
        self.part_data, self.part_count, self.data = particle_data, particle_count, data

    def encode(self) -> bytes:
        return (
            Buffer.pack("i", self.part_id)
            + Buffer.pack("?", self.long_dist)
            + Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("d", self.off_x)
            + Buffer.pack("d", self.off_y)
            + Buffer.pack("d", self.off_z)
            + Buffer.pack("f", self.part_data)
            + Buffer.pack("i", self.part_count)
            + Buffer.pack_particle(self.data)
        )
