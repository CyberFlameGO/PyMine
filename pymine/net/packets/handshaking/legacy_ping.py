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
"""Contains packets that support the legacy server list ping protocol."""

from __future__ import annotations

from pymine.types.buffer import Buffer
from pymine.types.packet import Packet

__all__ = (
    "HandshakeLegacyPingRequest",
    "HandshakeLegacyPingResponse",
)


class HandshakeLegacyPingRequest(Packet):
    """Request from the client asking for legacy ping response. (Client -> Server)

    :param int protocol: Protocol version being used, should now always be 74/4a.
    :param str hostname: The host/address the client is connecting to.
    :param int port: The port the client is connection on.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar protocol:
    :ivar hostname:
    :ivar port:
    """

    id = 0xFE
    to = 0

    def __init__(self, protocol: int, hostname: str, port: int) -> None:
        super().__init__()

        self.protocol = protocol
        self.hostname = hostname
        self.port = port

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeLegacyPingRequest:
        buf.read(15)
        return cls(buf.read(1), buf.read(buf.unpack("h")).decode("UTF-16BE"), buf.unpack("i"))


class HandshakeLegacyPingResponse(Packet):
    """Legacy response from the server to the client. Server -> Client

    :param str version: Version that the Minecraft server is running (i.e. 1.16.4).
    :param str motd: The server MOTD.
    :param int players_online: Amount of players currently on the server.
    :param int players_max: Maximum players allowed on the server.
    :ivar int id: Unique packet ID.
    :ivar version:
    :ivar motd:
    :ivar players_online:
    :ivar players_max:
    """

    id = 0xFF
    to = 1

    def __init__(self, version: str, motd: str, players_online: int, players_max: int) -> None:
        super().__init__()

        self.version = version
        self.motd = motd
        self.players_online = players_online
        self.players_max = players_max

    def encode(self) -> bytes:
        # Example:
        # b'\xff\x00\x23\x00\xa7\x00\x31\x00\x00\x00\x34\x00\x37\x00\x00\x00\x31\x00\x2e\x00\x34' \
        # b'\x00\x2e\x00\x32\x00\x00\x00\x41\x00\x20\x00\x4d\x00\x69\x00\x6e\x00\x65\x00\x63\x00' \
        # b'\x72\x00\x61\x00\x66\x00\x74\x00\x20\x00\x53\x00\x65\x00\x72\x00\x76\x00\x65\x00\x72' \
        # b'\x00\x00\x00\x30\x00\x00\x00\x32\x00\x30'

        out_string = f"§1\x00127\x00{self.motd}\x00{self.players_online}\x00{self.players_max}"
        return b"\xff" + Buffer.pack("h", len(out_string)) + out_string.encode("UTF-16BE")
