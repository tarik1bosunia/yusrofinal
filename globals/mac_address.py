import subprocess
from django.http import HttpResponse


def get_mac_address(request):
    client_ip = request.META.get('REMOTE_ADDR')
    print("client ip:", client_ip)
    output = subprocess.check_output(['arp', client_ip])
    output_lines = output.splitlines()
    mac_address = None
    for line in output_lines:
        line = line.decode('utf-8')
        if client_ip in line:
            mac_address = line.split()[2]
            break
    if mac_address:
        return HttpResponse(f"MAC address: {mac_address}")
    else:
        return HttpResponse("MAC address not found")