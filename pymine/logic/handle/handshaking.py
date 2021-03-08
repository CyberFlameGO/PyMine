from pymine.types.packet import Packet
from pymine.types.stream import Stream

from pymine.server import server


@server.api.register.on_packet("handshaking", 0x00)
async def handshake(stream: Stream, packet: Packet) -> None:
    server.cache.states[stream.remote] = packet.next_state
