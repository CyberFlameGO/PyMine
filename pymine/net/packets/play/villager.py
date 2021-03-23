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
"""Contains packets related to villager NPCs."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlaySelectTrade",
    "PlayTradeList",
)


class PlaySelectTrade(Packet):
    """Used when a player selects a specific trade offered by a villager. (Client -> Server)

    :param int selected_slot: The selected slot in the player's trade inventory.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar selected_slot:
    """

    id = 0x23
    to = 0

    def __init__(self, selected_slot: int) -> None:
        super().__init__()

        self.selected_slot = selected_slot

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySelectTrade:
        return cls(buf.unpack_varint())


class PlayTradeList(Packet):
    """Sends the list of trades a villager NPC is offering. (Server -> Client)

    :param int window_id: The trading GUI/window that is open.
    :param list trades: The trades to be sent.
    :param int villager_lvl: Level of the villager, one of: novice (1), apprentice (2), journeyman (3), expert (4), master (5).
    :param int xp: Total experience for that villager, 0 if the villager is a wandering one.
    :param bool is_regular: Whether the villager is a normal one or a wandering one.
    :param bool can_restock: True for regular villagers, false for wandering ones.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar window_id:
    :ivar trades:
    :ivar villager_lvl:
    :ivar xp:
    :ivar is_regular:
    :ivar can_restock:
    """

    id = 0x26
    to = 1

    def __init__(self, window_id: int, trades: list, villager_lvl: int, xp: int, is_regular: bool, can_restock: bool) -> None:
        super().__init__()

        self.window_id = window_id
        # We assume that a trade (entry in trades list) is a dictionary that contains trade data, see here: https://wiki.vg/Protocol#Trade_List
        # This is liable to change in the future as we decide how trades will be stored and loaded
        self.trades = trades
        self.villager_lvl = villager_lvl
        self.xp = xp
        self.is_regular = is_regular
        self.can_restock = can_restock

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.window_id)
            + Buffer.pack("b", len(self.trades))
            + b"".join([Buffer.pack_trade(**trade) for trade in self.trades])
            + Buffer.pack_varint(self.villager_lvl)
            + Buffer.pack_varint(self.xp)
            + Buffer.pack("?", self.is_regular)
            + Buffer.pack("?", self.can_restock)
        )
