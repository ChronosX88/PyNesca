from unittest import TestCase, main
from ipaddress import IPv4Address
from IpGenerator import IpGenerator
from Parser import Parser


class testIpGenerator(TestCase):

    def setUp(self):
        p = Parser()
        self.ipgen = IpGenerator(
        p.parse_address_field("192.168.1.1 - 192.168.1.10"), [80, 90])

    def testIpGeneration(self):
        '''self.assertEqual(
            self.ipgen.get_next_address(None),
            ("192.168.1.1", 80))'''
        previous_address = None
        a = True
        while previous_address or a:
             previous_address=self.ipgen.get_next_address(previous_address)
             a = False
        self.assertEqual(self.ipgen.get_next_address(None), None)


if __name__ == "__main__":
    main()
