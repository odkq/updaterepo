#!/usr/bin/env python
# simple updater for a trivial debian repository
import os
import gzip
import hashlib
import pexpect
from subprocess import *
p = Popen(['dpkg-scanpackages', '-m', '.'], stdout=PIPE, stderr=PIPE)
packages_s, e = p.communicate()
for file in ['Packages', 'Packages.gz', 'Release', 'Release.gpg']:
    if os.path.exists(file):
        os.remove(file)
pf = open('Packages', 'wb')
pfg = gzip.open('Packages.gz', 'wb')
pfg.write(packages_s)
pf.write(packages_s)
pfg.close()
pf.close()
release_header = '''Origin: You and your friends
Label: Some label
Codename: Squeeze
Date: Wed, 16 May 2012 12:37:30 UTC
Architectures: i386 amd64
Components: main
Description: A neat description
'''
f = open('Release','w')
f.write(release_header)
f.write('MD5Sum:\n')
for file in ['Packages', 'Packages.gz']:
    f.write(' ' +  hashlib.md5(open(file).read()).hexdigest())
    f.write(' ' + str(int(os.path.getsize(file))) + ' ' + file + '\n')
f.close()
child = pexpect.spawn('gpg --armor --sign --detach-sign --output=Release.gpg Release')
child.expect('Enter passphrase:', timeout=20)
child.sendline('yourgpgkeypassword\n')

