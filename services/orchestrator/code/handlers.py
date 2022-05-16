# Internal.
from asyncio import gather
from data import PeerRecord
from json import loads
from protocol import WelcomeMsg, OnboardgMsg, OffboardMsg


class RequestHandler(object):
    """
    Base request handler class.
    """
    def __init__(self, ws, active_ws, data_set, address_space) -> None:
        self.ws = ws
        self.active_ws = active_ws
        self.data_set = data_set
        self.address_space = address_space

    async def handle(self) -> None:
        pass

    async def broadcast(self, msg):
        """
        Non blocking message broadcast to all network peers.
        """
        await gather(*[ws.send(msg) for ws in self.active_ws - set([self.ws])])


class OnboardHandler(RequestHandler):
    async def handle(self) -> None:
        data = await self.ws.recv()
        data = loads(data)
        pub_key = data.get('pub_key')
        
        # Allocate new virtual ip for client.
        virt_ip = self.address_space.alloc()
        real_ip = self.ws.remote_address[0]
        record = PeerRecord(pub_key, real_ip, virt_ip)

        await self._respond_welcome(record)
        await self._broadcast(record)
        self.active_ws.add(self.ws)
        self.data_set.set(record)
    
    async def _respond_welcome(self, record):
        peers_records = self.data_set.get_all()
        msg = WelcomeMsg(record, peers_records)
        await self.ws.send(msg)
    
    async def _broadcast(self, record):
        msg = OnboardgMsg(record)
        await self.broadcast(msg)


class OffboardHandler(RequestHandler):
    async def handle(self) -> None:
        real_ip = self.ws.remote_address[0]
        try:
            record = self.data_set.pop(real_ip)
        except KeyError:
            return
        await self._broadcast(record)
        self.address_space.free(record.virt_ip)

    async def _broadcast(self, record):
        msg = OffboardMsg(record)
        await self.broadcast(msg)
