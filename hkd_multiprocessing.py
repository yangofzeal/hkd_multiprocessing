# -*- coding: utf-8 -*-
# HKD OBFUSCATE v4 - portable source payload, no marshal/code-object dependency.
# Protection is import-time only; protected functions have no per-call wrapper.
def _hkd_v4_bootstrap(_g):
    import binascii as _hb
    import hashlib as _hh
    import struct as _hs
    import zlib as _hz

    _b = (
        _hb.unhexlify('8283da5dcd6eb8ec3dab09aab9f6bf04b9bd9e58dbbc94c2cbad48768b1bf363e5399a2ecf89498972734dee775cec7f7d338c99acef9626fcec32cbddd46255156c41084a90f177d24814da5c7734c641a8b31439ec36baf57cf04882c345f7a22f9d4c748337b85d8bfc119762be027692166f349fe0bd2f4bace22c639a49'),
        _hb.unhexlify('a8450aac5085d9ab76c8d48f60e875bde5ebb87370499db3dcc73f79723982d1eae53af731e20c416c54d530c7d2c3ee30c148a467c96324389e3d2e50c92c8173981913d1bbda5fe12d3d8500c1aa6d24848125b87c922290c431d525ffa23b02edb17c5ee427f042a493ee465ce353a7fc7636dc2d6fa5655455a06d58b886'),
        _hb.unhexlify('1899852f0119d84b0d37bd6cf5b2d6b0e591809602e4233546ed16fb0347f6208ab07977b6bf2087804a43c46d5646ad36abe89a026463ceeb69229abf66f302e5bf0c9ddb9ad46c8c5f167cf9a4887780c7b2a24894900287e0546e3d3984ab7c4ea7a4ed039d7705694a99d65dca68154b25fcd8d94f2ea0a7f8c64bdd44a5'),
        _hb.unhexlify('f04aefa4ba729ffba59c029f58c5bb10625e6008fa98bc2a30e9358c2c135b92740d5e5bc73e79aea173c894a45281e0de6dfd2d9d65f5d8a1fe32e4084e6a2f3740b916a9d8269e75b149564eba84d9ab9dfe60c733420f6d74a0d48a7674ae06b2763a437b3653f0ca564bf345c4db08bd6a9ea0a0cda6e964bd4ddcbe615b'),
        _hb.unhexlify('19d2345b798dd2d80857108afa4c03a8c051801d6bc26c00a021b0681beb6bb1e44391b6af802a4b7f4047d1550ced8f15c116f49f7dacc4dd50199eabce4016a02b7644cfbbd68aa04720c6f44593697f6d27c5f8bf4e1466df1f39d8ddf9cf861737503c350bb3ba0eb8046c5a239ee6672b2b91c8fb926684aa3296924902'),
        _hb.unhexlify('3a39f42abcc6a8628d92eb6ef0ace4614f419fa21dadb542f1ae1a9b3d5dc95d1dce6c51b5fa54c100b6baf1dc48a5e3458021ddafb579eab93534b03d484ee8dc52d799cbf41711e82eb25aebec05530427029ca99eee65ebeacf2288557567ae332f48025b583298784d9d1d8bc1c8b859c124bafe8b00a64f1c69'),
        _hb.unhexlify('aa725d6b408adfc77bb36c91153cd2e71fe4da0cf06e31f30fff255192b27f6824d95229dd7a7d7f52012aa840deedb6c6b6690a1cf13cbebb4dd58ec96c56cd9cda79a32efb44d2fb0a52cca3fbf70a52f2e05a293f8e3f130e55bbdf2a113e65aff969cfbebed3a29f7b822b9c29ce5cb5df5812df8a4c731bb45ef388e349'),
        _hb.unhexlify('a19fc5bb4071026ab8355c3cf443137c288784eb52b80db510f207073c76a2a33041f99d23bd35899d07142282e6ae84ae7e68325a17a3415c306b3d29856a92e89b0a185c12e6db1ab56ef037641772170ab96d64012ee7a5da9e3629a939d1dfb7ebc6b2c34237b6dcf71ea541482c6d229676aa66d68e7169bf11ea7fc02f'),
        _hb.unhexlify('9076e2c6f0e869dc63d9b5c9a3bd6bd8a7aa2005810bd3a7aade1dbb0d1b59ff24158ddff211700e1fb15392e3d02eb071b6159f659b3f98c87e7ca3671acc12866900004b94fa9c6171164c326c4834b5990c68af21d932830c8b3c0741f63fcefd3e069b921a3042553cf22db78eea85ae063dde1974b78665da3080a0998b'),
    )
    _inv = (6, 7, 0, 2, 4, 1, 3, 8, 5)
    _leaves = (
        _hb.unhexlify('dad2cfbe49515f9481a3a55c97aeb4bae76375ef739e9df2fa8b3486d0b89e0d'),
        _hb.unhexlify('6e315892fb1c213f5014339baf6d7ddb719f0b4c62cdee26f9b7993b869106e2'),
        _hb.unhexlify('b1db70704623feaebfb5c0b8268379ef922edca6554dfcf01455160c6f3d225e'),
        _hb.unhexlify('d73f6113ae27ead49896ea99c499dee0b656a1a1b1938254fcb0c91253a50923'),
        _hb.unhexlify('a7967c937783e6ea136f00453b0acac59d83c44b278ef8e9ad72b4ef4be7b451'),
        _hb.unhexlify('4dbcfd2d84b4743c86efc12a679033fc5fe6c74f9d1f3e61c1fa5ea18e1ba5cd'),
        _hb.unhexlify('999952cb1e75871a26f58661d040eee4d392441b866cbd3870b8839afc87342d'),
        _hb.unhexlify('300dd57dadc2b1456433f3daa132f18b985285e04e99315a0dbb1c2e4ad88755'),
        _hb.unhexlify('bc7e686b6f4a506baa3ed023a1a4284e5bf1d37c6d6ae60c0622cb62eeadbe67'),
    )
    _root = _hb.unhexlify('634feaea211bcde1af72db07e0f854f16ceb93c727538da85353352971b3f9eb')
    _share1 = _hb.unhexlify('55eda5f163d89abc0fa9ee2f50360fb8a1798cbdee89b7724aa601d666ef165c')
    _share2 = _hb.unhexlify('9f79c9c5af812421529d38fa0edc11dc26853438e917cd18eb1ba098b56c4e3b')

    def _u32(_n):
        return _hs.pack('>I', _n)

    def _xor(_a, _c):
        _o = bytearray(len(_a))
        _i = 0
        while _i < len(_a):
            _o[_i] = _a[_i] ^ _c[_i]
            _i += 1
        return bytes(_o)

    def _ks(_key, _index, _length):
        _o = bytearray()
        _counter = 0
        _seed = _key + _u32(_index)
        while len(_o) < _length:
            _o.extend(_hh.sha256(_seed + _u32(_counter)).digest())
            _counter += 1
        return bytes(_o[:_length])

    def _merkle(_values):
        if not _values:
            return _hh.sha256(b'').digest()
        _level = list(_values)
        while len(_level) > 1:
            if len(_level) & 1:
                _level.append(_level[-1])
            _next = []
            _i = 0
            while _i < len(_level):
                _next.append(_hh.sha256(_level[_i] + _level[_i + 1]).digest())
                _i += 2
            _level = _next
        return _level[0]

    _key = _xor(_share1, _share2)
    _parts = []
    _verify = []
    _i = 0
    while _i < len(_inv):
        _masked = _b[_inv[_i]]
        _raw = _xor(_masked, _ks(_key, _i, len(_masked)))
        _parts.append(_raw)
        _verify.append(_hh.sha256(_u32(_i) + _raw).digest())
        _i += 1

    if tuple(_verify) != _leaves or _merkle(_verify) != _root:
        raise ImportError('HKD protected payload integrity verification failed')

    try:
        _source = _hz.decompress(b''.join(_parts)).decode('utf-8')
    except Exception as _exc:
        raise ImportError('HKD protected payload reconstruction failed: %s' % (_exc,))

    _filename = _g.get('__file__') or '<HKD-obfuscated>'
    _code = compile(_source, _filename, 'exec', 0, True, 0)

    # Discard the plaintext string before running user code.  CPython may reclaim
    # it immediately; no plaintext source is retained as a module global.
    del _source

    # Exact module semantics: definitions execute in the actual module globals.
    exec(_code, _g, _g)

_hkd_v4_bootstrap(globals())
del _hkd_v4_bootstrap
