# Builtin.
from os import environ

# Internal.
from server import WSServer


def get_args():
    port, netmask = environ.get('PORT'), environ.get('NETMASK')
    if not port:
        raise 'Missing port variable'
    if not netmask:
        raise 'Missing netmask variable'
    return port, netmask


def main():
    port, netmask = get_args()
    server = WSServer('0.0.0.0', port, netmask)
    server.serve_forever()
    

if __name__ == '__main__':
    main()
