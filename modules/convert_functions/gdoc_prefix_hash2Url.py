def gdocs_prefix_hash2Url(prefix:'gdoc_prefix', ghash:'gdoc_hash') -> {'url'}:
    return {'url':prefix + ghash}
