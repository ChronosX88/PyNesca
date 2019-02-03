from unittest import main, TestCase
from Parser import Parser
import ipaddress


class TestParser(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_port_parsing(self):
        self.assertEqual(self.parser.parse_port_field("80,90"), [80, 90])

    def test_ip_parsing(self):
        self.assertEqual(
            set(self.parser.parse_address_field("192.168.1.1 - 192.168.1.3")),
            {ipaddress.IPv4Address(ip) for ip in
                [
                "192.168.1.1",
                "192.168.1.2",
                "192.168.1.3"
                ]})
        self.assertEqual(
            set(self.parser.parse_address_field("192.168.1.1")),
            {ipaddress.IPv4Address("192.168.1.1")}
            )
        self.assertEqual(
            set(self.parser.parse_address_field("192.168.1.0/31")),
            {ipaddress.IPv4Address(ip) for ip in
                [
                '192.168.1.1',
                '192.168.1.0'
                ]})


if __name__ == "__main__":
    main()
