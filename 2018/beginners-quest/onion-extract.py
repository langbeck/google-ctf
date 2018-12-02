#!/usr/bin/python3
import zipfile
import lzma
import gzip
import bz2
import sys
import io

name = 'password.x.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p'
with open(name, 'rb') as fp:
    data = fp.read()


sys.stderr.write('# zip:  ')
try:
    while True:
        zf = zipfile.ZipFile(io.BytesIO(data))
        data = zf.read(zf.namelist()[0])
        sys.stderr.write('.')

except zipfile.BadZipFile:
    pass


sys.stderr.write('\n# lzma: ')
try:
    while True:
        data = lzma.decompress(data)
        sys.stderr.write('.')
except lzma.LZMAError:
    pass


sys.stderr.write('\n# bz2:  ')
try:
    while True:
        data = bz2.decompress(data)
        sys.stderr.write('.')
except OSError:
    pass


sys.stderr.write('\n# gzip: ')
try:
    while True:
        data = gzip.decompress(data)
        sys.stderr.write('.')
except OSError:
    pass


sys.stderr.write('\n')
sys.stderr.flush()



password_data = None
zip = zipfile.ZipFile(io.BytesIO(data))
with open('10-million-password-list-top-1000000.txt', 'rb') as fp:
    for pwd in fp:
        try:
            password_data = zip.read(zip.filelist[0], pwd=pwd.rstrip())
            break
        except RuntimeError:        pass
        except zipfile.BadZipFile:  pass
        


if password_data:
    print(password_data.decode('utf8'))


with open('password.zip', 'wb') as fp:
    fp.write(data)


