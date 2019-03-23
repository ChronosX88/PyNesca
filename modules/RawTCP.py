from struct import pack, unpack
import socket


class TCPHeader():
    # TCP header class. Thanks to Silver Moon for the flags calculation and packing order
    # This was designed to be re-used. You might want to randomize the seq number
    # get_struct performs packing based on if you have a valid checksum or not
    def __init__(self, src_port=47123, dst_port=80, seqnum=1000, acknum=0, data_offset=80, fin=0, syn=1, rst=0, psh=0, ack=0, urg=0, window=5840, check=0, urg_ptr=0):
        # !=network(big-endian), H=short(2), L=long(4),B=char(1)
        self.order = "!HHLLBBHHH"
        self.src_port = src_port
        self.dst_port = dst_port
        self.seqnum = seqnum
        self.acknum = acknum
        # size of tcp header; size is specified by 4-byte words; This is 80
        # decimal, which is 0x50, which is 20bytes (5words*4bytes).
        self.data_offset = data_offset
        self.fin = fin
        self.syn = syn
        self.rst = rst
        self.psh = psh
        self.ack = ack
        self.urg = urg
        self.window = socket.htons(window)
        self.check = check
        self.urg_ptr = urg_ptr

    def flags(self):
        return self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh << 3) + (self.ack << 4) + (self.urg << 5)

    def get_struct(self, check=False, checksummed=False):
        if check is not False:
            self.check = check
        if checksummed:
            return pack('!HHLLBBH', self.src_port, self.dst_port, self.seqnum, self.acknum, self.data_offset, self.flags(), self.window) + pack('H', self.check) + pack('!H', self.urg_ptr)
        else:
            return pack(self.order, self.src_port, self.dst_port, self.seqnum, self.acknum, self.data_offset, self.flags(), self.window, self.check, self.urg_ptr)


def checksum(msg):
    # Shoutout to Silver Moon @ binarytides for this checksum algo.
    sum = 0
    for i in range(0, len(msg), 2):
        w = msg[i] + (msg[i + 1] << 8)
        sum = sum + w

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    sum = ~sum & 0xffff
    return sum


def tcp_checksum(source_ip, dest_ip, tcp_header, user_data=b''):
    # Calculates the correct checksum for the tcp header
    tcp_length = len(tcp_header) + len(user_data)
    # This is an IP header w/ TCP as protocol.
    ip_header = pack('!4s4sBBH', socket.inet_aton(source_ip), socket.inet_aton(
        dest_ip), 0, socket.IPPROTO_TCP, tcp_length)
    # Assemble the packet (IP Header + TCP Header + data, and then send it to
    # checksum function)
    packet = ip_header + tcp_header + user_data
    return checksum(packet)


def handle_packet(raw_packet):
    # Now we need to unpack the packet. It will be an IP/TCP packet
    # We are looking for SYN-ACKs from our SYN scan
    # Fields to check: IP - src addr; TCP - src port, flags
    # We want to pull out and compare only these three
    # Heres the math for unpacking: B=1, H=2, L=4, 4s=4  (those are bytes)
    packet = raw_packet[0]
    # This is the IP header, not including any self.options OR THE DST ADDR.
    # Normal length is 20!! Im parsing as little as possible
    ip_header = unpack('!BBHHHBBH4s', packet[0:16])
    # If there are any self.options, the length of the IP header will be >20. We
    # dont care about self.options
    ip_header_length = (ip_header[0] & 0xf) * 4
    # This is the source address (position 8, or the first "4s" in our
    # unpack)
    src_addr = socket.inet_ntoa(ip_header[8])

    # We had to get the proper IP Header length to find the TCP header
    # offset.
    tcp_header_raw = packet[ip_header_length:ip_header_length + 14]
    # TCP header structure is pretty straight-forward. We want PORTS and
    # FLAGS, so we partial unpack it
    tcp_header = unpack('!HHLLBB', tcp_header_raw)

    src_port = tcp_header[0]  # self-explanatory
    dst_port = tcp_header[1]  # self-explanatory FIXME: notused
    # We only care about syn-ack, which will be 18 (0x12)
    flag = tcp_header[5]

    if flag == 18:
        return (src_addr, src_port)
    else:
        return None
