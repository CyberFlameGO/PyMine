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

"""For packets related to structure/jigsaw blocks."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayGenerateStructure", "PlayUpdateJigsawBlock", "PlayUpdateStructureBlock")


class PlayGenerateStructure(Packet):
    """Sent by the client when the generate button is pressed on a jigsaw block. (Client -> Server)

    :param int x: The x coordinate of the jigsaw block.
    :param int y: The y coordinate of the jigsaw block.
    :param int z: The z coordinate of the jigsaw block.
    :param int levels: The value of the levels slider in the block interface.
    :param bool keep_jigsaws: Unknown.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar levels:
    :ivar keep_jigsaws:
    """

    id = 0x0F
    to = 0

    def __init__(self, x: int, y: int, z: int, levels: int, keep_jigsaws: bool) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.levels = levels
        self.keep_jigsaws = keep_jigsaws

    @classmethod
    def decode(cls, buf: Buffer) -> PlayGenerateStructure:
        return cls(*buf.unpack_position(), buf.unpack_varint(), buf.unpack("?"))


class PlayUpdateJigsawBlock(Packet):
    """Sent when done is pressed on a jigsaw block. See here: https://wiki.vg/Protocol#Update_Jigsaw_Block (Client -> Server)

    :param int x: The x coordinate of the jigsaw block.
    :param int y: The y coordinate of the jigsaw block.
    :param int z: The z coordinate of the jigsaw block.
    :param str name: The name.
    :param str target: The target.
    :param str pool: The pool.
    :param str final_state: "Turns into" on the GUI, final_state in NBT.
    :param str joint_type: rollable if the attached piece can be rotated, else aligned.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar name:
    :ivar target:
    :ivar pool:
    :ivar final_state:
    :ivar joint_type:
    """

    id = 0x29  # Might be 0x28?? See here: https://wiki.vg/Protocol#Update_Jigsaw_Block
    to = 0

    def __init__(self, x: int, y: int, z: int, name: str, target: str, pool: str, final_state: str, joint_type: str) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.name = name
        self.target = target
        self.pool = pool
        self.final_state = final_state
        self.joint_type = joint_type

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateJigsawBlock:
        return cls(
            *buf.unpack_position(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string(),
        )


class PlayUpdateStructureBlock(Packet):
    """Sent by the client to update a structure block. (Client -> Server)

    :param int x: The x coordinate of the structure block.
    :param int y: The y coordinate of the structure block.
    :param int z: The z coordinate of the structure block.
    :param int action: An additional action to perform other than saving the data, see here: https://wiki.vg/Protocol#Update_Structure_Block
    :param int mode: One of: save (0), load (1), corner (2), data (3).
    :param str name: The name of the structure.
    :param int offset_x: The x offset (between -32 and 32).
    :param int offset_y: The y offset (between -32 and 32).
    :param int offset_z: The z offset (between -32 and 32).
    :param int size_x: The x axis size (between -32 and 32).
    :param int size_y: The y axis size (between -32 and 32).
    :param int size_z: The z axis size (between -32 and 32).
    :param int mirror: One of: none (0), left_right (1), front_back (2).
    :param int rotation: One of: none (0), clockwise 90 (1), clockwise 180 (2), counter-clockwise 90 (3).
    :param str metadata: Additional metadata.
    :param float integrity: Integrity between 0 and 1.
    :param int seed: Unknown.
    :param int flags: Additional flags, see here: https://wiki.vg/Protocol#Update_Structure_Block.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar action:
    :ivar mode:
    :ivar name:
    :ivar offset_x:
    :ivar offset_y:
    :ivar offset_z:
    :ivar size_x:
    :ivar size_y:
    :ivar size_z:
    :ivar mirror:
    :ivar rotation:
    :ivar metadata:
    :ivar integrity:
    :ivar seed:
    :ivar flags:
    """

    id = 0x2A
    to = 0

    def __init__(
        self,
        x: int,
        y: int,
        z: int,
        action: int,
        mode: int,
        name: str,
        offset_x: int,
        offset_y: int,
        offset_z: int,
        size_x: int,
        size_y: int,
        size_z: int,
        mirror: int,
        rotation: int,
        metadata: str,
        integrity: float,
        seed: int,
        flags: int,
    ) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.action = action
        self.mode = mode
        self.name = name
        self.offset_x, self.offset_y, self.offset_z = offset_x, offset_y, offset_z
        self.size_x, self.size_y, self.size_z = size_x, size_y, size_z
        self.mirror = mirror
        self.rotation = rotation
        self.metadata = metadata
        self.integrity = integrity
        self.seed = seed
        self.flags = flags

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateStructureBlock:
        return cls(
            *buf.unpack_position(),
            buf.unpack_varint(),
            buf.unpack_varint(),
            buf.unpack_string(),
            buf.unpack("b"),
            buf.unpack("b"),
            buf.unpack("b"),
            buf.unpack("b"),
            buf.unpack("b"),
            buf.unpack("b"),
            buf.unpack_varint(),
            buf.unpack_varint(),
            buf.unpack_string(),
            buf.unpack("f"),
            buf.unpack_varint(),
            buf.unpack("b"),
        )
