#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, Extension

import sys
import platform
import struct
import os

includes = []
libraries = []
library_dirs = []
extra_sources = []
CFLAGS = []


if sys.platform.startswith('linux'):
    define_macros = [('HAVE_CLOCK_GETTIME', '1'),
                     ('HAVE_LIBRT', '1'),
                     ('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_STRUCT_SYSINFO', '1'),
                     ('HAVE_STRUCT_SYSINFO_MEM_UNIT', '1'),
                     ('HAVE_STRUCT_SYSINFO_TOTALRAM', '1'),
                     ('HAVE_SYSINFO', '1'),
                     ('HAVE_SYS_SYSINFO_H', '1'),
                     ('_FILE_OFFSET_BITS', '64')]
    libraries = ['crypto', 'rt']
    includes = ['/usr/local/include', '/usr/include']
    CFLAGS.append('-O2')
elif sys.platform.startswith('win32'):
    define_macros = [('inline', '__inline')]

    extra_sources = ['scrypt-windows-stubs/gettimeofday.c']
    if struct.calcsize('P') == 8:
        if os.path.isdir('c:\OpenSSL-v111-Win64') and sys.version_info[0] >= 3 and sys.version_info[1] > 4:
            openssl_dir = 'c:\OpenSSL-v111-Win64'
        else:
            openssl_dir = 'c:\OpenSSL-Win64'
        library_dirs = [openssl_dir + '\lib']
        includes = [openssl_dir + '\include', 'scrypt-windows-stubs/include']
    else:
        if os.path.isdir('c:\OpenSSL-v111-Win32'):
            openssl_dir = 'c:\OpenSSL-v111-Win32'
        else:
            openssl_dir = 'c:\OpenSSL-Win32'
        library_dirs = [openssl_dir + '\lib']
        includes = [openssl_dir + '\include', 'scrypt-windows-stubs/include']
    windows_link_legacy_openssl = os.environ.get(
        "SCRYPT_WINDOWS_LINK_LEGACY_OPENSSL", None
    )
    if  windows_link_legacy_openssl is None:
        libraries = ['libcrypto_static']
    else:
        libraries = ['libeay32']
    libraries += ["advapi32", "gdi32", "user32", "ws2_32"]

elif sys.platform.startswith('darwin') and platform.mac_ver()[0] < '10.6':
    define_macros = [('HAVE_SYSCTL_HW_USERMEM', '1')]
        # disable for travis
    libraries = ['crypto']
elif sys.platform.startswith('darwin'):
    define_macros = [('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_SYSCTL_HW_USERMEM', '1')]
        # disable for travis
    libraries = ['crypto']
else:
    define_macros = [('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_SYSCTL_HW_USERMEM', '1')]
    libraries = ['crypto']

scrypt_module = Extension(
    '_scrypt',
    sources=['src/scrypt.c',
             'scrypt-1.2.1/lib/crypto/crypto_scrypt_smix_sse2.c',
             'scrypt-1.2.1/lib/crypto/crypto_scrypt_smix.c',
             'scrypt-1.2.1/lib/crypto/crypto_scrypt.c',
             'scrypt-1.2.1/lib/scryptenc/scryptenc.c',
             'scrypt-1.2.1/lib/scryptenc/scryptenc_cpuperf.c',
             'scrypt-1.2.1/lib/util/memlimit.c',
             'scrypt-1.2.1/libcperciva/alg/sha256.c',
             'scrypt-1.2.1/libcperciva/crypto/crypto_aes_aesni.c',
             'scrypt-1.2.1/libcperciva/crypto/crypto_aes.c',
             'scrypt-1.2.1/libcperciva/crypto/crypto_aesctr.c',
             'scrypt-1.2.1/libcperciva/crypto/crypto_entropy.c',
             'scrypt-1.2.1/libcperciva/util/entropy.c',
             'scrypt-1.2.1/libcperciva/util/insecure_memzero.c',
             'scrypt-1.2.1/libcperciva/util/warnp.c',
             'scrypt-1.2.1/libcperciva/util/humansize.c',
             'scrypt-1.2.1/libcperciva/util/asprintf.c'] + extra_sources,
    include_dirs=['scrypt-1.2.1',
                  'scrypt-1.2.1/lib',
                  'scrypt-1.2.1/lib/scryptenc',
                  'scrypt-1.2.1/lib/crypto',
                  'scrypt-1.2.1/lib/util',
                  'scrypt-1.2.1/libcperciva/cpusupport',
                  'scrypt-1.2.1/libcperciva/alg',
                  'scrypt-1.2.1/libcperciva/util',
                  'scrypt-1.2.1/libcperciva/crypto'] + includes,
    define_macros=[('HAVE_CONFIG_H', None)] + define_macros,
    extra_compile_args=CFLAGS,
    library_dirs=library_dirs,
    libraries=libraries)

setup(name='scrypt',
      version='0.8.17',
      description='Bindings for the scrypt key derivation function library',
      author='Magnus Hallin',
      author_email='mhallin@gmail.com',
      maintainer="Holger Nahrstaedt",
      maintainer_email="holgernahrstaedt@gmx.de",
      url='https://github.com/holgern/py-scrypt',
      packages=['scrypt', 'scrypt.tests'],
      package_data={'scrypt': ['tests/*.csv']},
      ext_modules=[scrypt_module],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: Security :: Cryptography',
                   'Topic :: Software Development :: Libraries'],
      license='2-clause BSD',
      long_description=open('README.rst').read())
