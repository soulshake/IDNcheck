# -*- coding: utf-8 -*-
from idncheck import idncheck


DATA = u"""
1 hello
2 ηελλο
3 hぇllぉ
4 hﻫllة
5 hελλo
#3 hελλo.com
5 hελλø
# 6 hell♥
"""

MAXLEVEL = 6


def verify(result, func, *args):
    assert result == func(*args)


def test():
    for line in DATA.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        level, domain = line.split()
        level = int(level)
        yield verify, level, idncheck, domain
        # FIXME enable this later, once the API can handle it
        #for sublevel in range(1, MAXLEVEL+1):
        #    yield verify, (sublevel <= level), idncheck, domain, sublevel
