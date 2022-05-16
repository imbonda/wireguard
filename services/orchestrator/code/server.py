# 3rd party.
from asyncio import get_event_loop, new_event_loop, set_event_loop
from websockets import serve, ConnectionClosed

# Internal.
from address_space import AddressSpace, AddressSpaceExhausted
from data import DataSet
from handlers import OnboardHandler, OffboardHandler


class WSServer(object):
    def __init__(self, server_ip, port, netmask) -> None:
        self.port = port
        self.server_ip = server_ip
        self.data_set = DataSet()
        self.address_space = AddressSpace(netmask)
        self.active_ws = set()

    def serve_forever(self):
        loop = new_event_loop()
        set_event_loop(loop)
        start_server = serve(self.handler, self.server_ip, self.port)
        get_event_loop().run_until_complete(start_server)
        get_event_loop().run_forever()

    async def handler(self, ws, _):
        if not self.is_new_client(ws):
            await ws.send('Already onboard')
            return

        try:
            await OnboardHandler(ws, self.active_ws, self.data_set, self.address_space).handle()
        except AddressSpaceExhausted:
            await ws.send('No available IP address')
            return

        while True:
            try:
                # Keep socket active until closed by client.
                await ws.recv()
            except ConnectionClosed:
                await OffboardHandler(ws, self.active_ws, self.data_set, self.address_space).handle()
                break
    
    def is_new_client(self, ws):
        client_ip = ws.remote_address[0]
        active_client_ips = {ws.remote_address[0] for ws in self.active_ws}
        if client_ip in active_client_ips:
            return False
        return True
