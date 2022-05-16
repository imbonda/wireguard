# Builtin.
from enum import IntEnum
from json import dumps


class MessageType(IntEnum):
    """
    The different types of messages sent to peers over the orchestration lifecycle.
    """
    WELCOME = 1
    ONBOARD = 2
    OFFBOARD = 3


WelcomeMsg = lambda record, peers_records: dumps({
    'type': MessageType.WELCOME,
    'ip': record.virt_ip,
    'peers': [(r.virt_ip, r.pub_key) for r in peers_records],
})
OnboardgMsg = lambda record: dumps({
    'type': MessageType.ONBOARD,
    'ip': record.virt_ip,
    'pub_key': record.pub_key,
})
OffboardMsg = lambda record: dumps({
    'type': MessageType.OFFBOARD,
    'ip': record.virt_ip,
})
