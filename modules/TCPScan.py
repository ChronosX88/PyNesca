from RawTCP import TCPHeader, handle_packet, tcp_checksum
import socket
import sys


class TCPScanner:
    def __init__(self):
        self.source_ips = {}
        # TODO: options, threading, input/output queues
        self.options = None
        return

    def in_scope(self):
        """Check that IP is in scanning scope"""
        # TODO
        pass

    def tcp_listener(self):
        # Raw socket listener for when send_raw_syn() is used. This will catch
        # return SYN-ACKs
        listen = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        while True:
            # packet = ('E \x00(\x1f\xaa@\x00w\x06\x99w2\xe0\xc8\xa2\xa2\xf3\xac\x18\xdf\xb3\x00\x16\xb6\x80\xc1\xa0/\xa6=$P\x10\xce\xab\xd1\xe4\x00\x00', ('50.XXX.200.162', 0))
            raw_packet = listen.recvfrom(65565)
            ret = handle_packet(raw_packet)
            if ret is None:
                continue
            src_addr, src_port = ret
            if self.in_scope(src_addr) and src_port in self.ports:
                self.output_queue.put((src_addr, src_port))

    def send_raw_syn(self, dest_ip, dst_port):
        # Use raw sockets to send a SYN packet.
        # If you want, you could use the IP header assembled in the tcp_checksum
        # function to have a fully custom TCP/IP stack
        try:
            # Using IPPROTO_TCP so the kernel will deal with the IP packet for us.
            # Change to IPPROTO_IP if you want control of IP header as well
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except Exception:
            sys.stderr.write("Error creating socket in send_raw_syn\n")
            return
        if self.options.source == "auto":
            # This gets the correct source IP. Just in case of multiple interfaces,
            # it will pick the right one
            src_addr = self.get_source_ip(dest_ip)
        else:
            src_addr = self.options.source
        src_port = 54321
        make_tcpheader = TCPHeader(src_port, dst_port)
        tcp_header = make_tcpheader.get_struct()
        packet = make_tcpheader.get_struct(check=tcp_checksum(
            src_addr, dest_ip, tcp_header), checksummed=True)
        try:
            s.sendto(packet, (dest_ip, 0))
        except Exception as e:
            sys.stderr.write("Error utilizing raw socket in send_raw_syn: {}\n".format(e))

    def get_source_ip(self, dst_addr):
        # Credit: 131264/alexander from stackoverflow. This gets the correct IP for sending. Useful if you have multiple interfaces
        # NOTE: This will send an additional packet for every single IP to confirm
        # the route. (but just one packet)
        try:
            if dst_addr in self.source_ips:
                return self.source_ips[dst_addr]
            else:
                self.source_ips[dst_addr] = [(s.connect((dst_addr, 53)), s.getsockname()[0], s.close(
                )) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
                return self.source_ips[dst_addr]
        except Exception:
            sys.stderr.write(
                "Something went wrong in get_source_ip, results might be wrong\n")


def send_full_connect_syn(ip, port, timeout):
    # Normal scan using socket to connect. Does 3-way handshack, then graceful
    # teardown using FIN
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
    except Exception as e:
        sys.stderr.write("Error creating socket in send_full_connect_syn: {}\n".format(e))
        return False
    try:
        s.connect((ip, port))
        return True
        s.close()
    except Exception:
        return False
