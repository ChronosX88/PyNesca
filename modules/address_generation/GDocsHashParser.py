from core.prototypes.AbstractParser import AbstractParser

class GDocsHashParser(AbstractParser):

    def parse_fields(self, afield:"address_field") -> {"gdocs_prefix",
    "gdocs_hash_ranges"}:
        split_index = afield.find(" ")
        prefix = afield[:split_index].strip()
        hash_ranges = [hr.strip() for hr in afield[split_index:].split(",")]
        result = []
        for hr in hash_ranges:
            if " - " in hr:
                result.append(hr.split(" - "))
            else:
                result.append([hr, hr])
        return {
            "gdocs_prefix":prefix,
            "gdocs_hash_ranges":result
        }
