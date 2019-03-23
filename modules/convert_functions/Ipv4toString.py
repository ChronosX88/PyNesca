from core.communication.ConvertTable import convert_function

@convert_function("ipv4","str")
def ipv4tostring(ip):
    return str(ip)
