from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.stream import Stream
from pymine.types.chat import Chat

import pymine.net.packets.status.status as status_packets

from pymine.api.errors import StopHandling
from pymine.server import server


@server.api.events.on_packet("status", 0x00)
async def send_status(stream: Stream, packet: Packet) -> tuple:
    data = {
        "version": {"name": server.meta.version, "protocol": server.meta.protocol},
        "players": {
            "max": server.conf["max_players"],
            "online": len(server.cache.states),
            "sample": [
                {"name": "Iapetus11", "id": "cbcfa252-867d-4bda-a214-776c881cf370"},
                {"name": "Sh_wayz", "id": "cbcfa252-867d-4bda-a214-776c881cf370"},
                {"name": "emeralddragonmc", "id": "eb86dc19-c3f5-4aef-a50e-a4bf435a7528"},
            ],
        },
        "description": Chat(server.conf["motd"]).msg,  # a Chat
    }

    if server.favicon:
        data["favicon"] = server.favicon

    await server.send_packet(stream, status_packets.StatusStatusResponse(data), -1)


@server.api.events.on_packet("status", 0x01)
async def send_pong(stream: Stream, packet: Packet) -> tuple:
    await server.send_packet(stream, packet, -1)
    raise StopHandling
