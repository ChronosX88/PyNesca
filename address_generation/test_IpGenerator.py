from unittest import TestCase, main
from ipaddress import IPv4Address
from IpGenerator import IpGenerator
from Parser import Parser


class testIpGenerator(TestCase):

    def setUp(self):
        p = Parser()
        self.ipgen = IpGenerator(p.parse_address_field("192.168.1.1"), [80])

    def testIpGeneration(self):
        self.assertEquals(
            self.ipgen.get_next_address(None),
            (IPv4Address("192.168.1.1"), 80))
        print(self.ipgen.get_next_address(None))


if __name__ == "__main__":
    main()
