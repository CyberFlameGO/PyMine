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

"""Contains packets relating to client logins."""

from __future__ import annotations
import secrets
import uuid

from pymine.types.buffer import Buffer
from pymine.types.packet import Packet
from pymine.types.chat import Chat

__all__ = (
    "LoginStart",
    "LoginEncryptionRequest",
    "LoginEncryptionResponse",
    "LoginSuccess",
    "LoginDisconnect",
)


class LoginStart(Packet):
    """Packet from client asking to start login process. (Client -> Server)

    :param str username: Username of the client who sent the request.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar username:
    """

    id = 0x00
    to = 0

    def __init__(self, username: str) -> None:
        super().__init__()

        self.username = username

    @classmethod
    def decode(cls, buf: Buffer) -> LoginStart:
        return cls(buf.read(buf.unpack_varint()).decode("UTF-8"))


class LoginEncryptionRequest(Packet):
    """Used by the server to ask the client to encrypt the login process. (Server -> Client)

    :param bytes public_key: Public key.
    :ivar type verify_token: Verify token, randomly generated.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar public_key:
    """

    id = 0x01
    to = 1

    def __init__(self, public_key: bytes) -> None:  # https://wiki.vg/Protocol#Encryption_Request
        super().__init__()

        self.public_key = public_key
        self.verify_token = secrets.token_bytes(16)

    def encode(self) -> bytes:
        return (
            Buffer.pack_string(" " * 20)
            + Buffer.pack_varint(len(self.public_key))
            + self.public_key
            + Buffer.pack_varint(len(self.verify_token))
            + self.verify_token
        )


class LoginEncryptionResponse(Packet):
    """Response from the client to a LoginEncryptionRequest. (Client -> Server)

    :param bytes shared_key: The shared key used in the login process.
    :param bytes verify_token: The verify token used in the login process.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar shared_key:
    :ivar verify_token:
    """

    id = 0x01
    to = 0

    def __init__(self, shared_key: bytes, verify_token: bytes) -> None:
        super().__init__()

        self.shared_key = shared_key
        self.verify_token = verify_token

    @classmethod
    def decode(cls, buf: Buffer) -> LoginEncryptionResponse:
        return cls(buf.read(buf.unpack_varint()), buf.read(buf.unpack_varint()))


class LoginSuccess(Packet):
    """Sent by the server to denote a successfull login. (Server -> Client)

    :param uuid.UUID uuid: The UUID of the connecting player/client.
    :param str username: The username of the connecting player/client.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar uuid:
    :ivar username:
    """

    id = 0x02
    to = 1

    def __init__(self, uuid_: uuid.UUID, username: str) -> None:
        super().__init__()

        self.uuid = uuid_
        self.username = username

    def encode(self) -> bytes:
        return Buffer.pack_uuid(self.uuid) + Buffer.pack_string(self.username)


class LoginDisconnect(Packet):
    """Sent by the server to kick a player while in the login state. (Server -> Client)

    :param str reason: The reason for the disconnect.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar username:
    """

    id = 0x00
    to = 1

    def __init__(self, reason: str) -> None:
        super().__init__()

        self.reason = reason

    def encode(self) -> bytes:
        return Buffer.pack_chat(Chat(self.reason))
