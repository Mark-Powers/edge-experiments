import xmlrpc.client
import sys


def log_event(name, details):
    s = xmlrpc.client.ServerProxy('http://localhost:8000')
    s.log(name, details)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ./rpc_client.py event_type details...")
        sys.exit()
    log_event(sys.argv[1], *sys.argv[2:])
