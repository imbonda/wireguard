# Builtin.
from ipaddress import ip_network


class AddressSpaceExhausted(Exception):
    pass


class AddressSpace(object):
    def __init__(self, netmask) -> None:
        self.hosts = iter(ip_network(netmask).hosts())
        self.reusable = set()
    
    def alloc(self) -> str:
        """
        Allocating new ip address.

        :return: Newly allocated ip address.
        """
        if self.reusable:
            return self.reusable.pop()
        try:
            return str(next(self.hosts))
        except StopIteration:
            raise AddressSpaceExhausted()

    def free(self, ip) -> None:
        """
        Free the allocated ip address.

        :param ip: Ip address to free.
        """
        self.reusable.add(ip)
