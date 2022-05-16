from collections import namedtuple

PeerRecord = namedtuple('Record', ['pub_key', 'real_ip', 'virt_ip'])


class DataSet(object):
    """
    In memory data store.
    """
    def __init__(self) -> None:
        self._record_by_ip = {}

    def exists(self, real_ip) -> bool:
        return self._record_by_ip.get(real_ip) is not None

    def set(self, record) -> None:
        self._record_by_ip[record.real_ip] = record

    def pop(self, real_ip) -> None:
        return self._record_by_ip.pop(real_ip)

    def get_all(self):
        return self._record_by_ip.values()
