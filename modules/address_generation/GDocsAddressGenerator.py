from core.prototypes.AbstractAddressGenerator import AbstractAddressGenerator
from core.prototypes.AbstractModuleClass import internal

class GDocsAddressGenerator(AbstractAddressGenerator):
    def set_parsed_fields(self, prefix:"gdocs_prefix",
    ranges:"gdocs_hash_ranges") -> None: 
        self.alphabet = list(
            '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
        )
        self.revsymbols = {symb:i for i, symb in enumerate(self.alphabet)}
        self.prefix = prefix
        self.ranges = ranges
        self.hashlen = len(ranges[0][0])
        self.currange = self.ranges.pop(0)  

    @internal
    def hash2int(self, gdhash):
        alen = len(self.alphabet)
        res = 0
        for symb in gdhash:
            res *= alen
            res += self.revsymbols[symb]
        return res

    @internal
    def int2hash(self, hint):
        alen = len(self.alphabet)
        reshash = [self.alphabet[0]]*self.hashlen
        for i in range(-1, -self.hashlen-1, -1):
           hint, rest = divmod(hint, alen)
           reshash[i] = self.alphabet[rest]
        return "".join(reshash)

    def get_next_address(self, prev_url:'url') -> {"url"}: 
        if not prev_url: 
            return {'url':self.prefix + self.currange[0]}
        prev_hash = prev_url[prev_url.rfind('/') + 1:]
        if self.hash2int(self.currange[1]) <= self.hash2int(prev_hash):
            if not self.ranges: return None
            self.currange = self.ranges.pop(0)
            return {'url' : self.prefix + self.currange[0]}
        return {'url' : self.prefix + self.int2hash(self.hash2int(prev_hash) +
        1)}

    def get_all_addresses(self) -> {'gdocs_prefix', 'gdocs_hash_ranges'}:
        return {'gdocs_prefix':self.prefix, 'gdocs_hash_ranges': self.ranges}
