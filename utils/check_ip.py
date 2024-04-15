import ipaddress


def check_ip_match_the_mask(ip, mask):
    ip_network = ipaddress.ip_network(mask)
    return ipaddress.ip_address(ip) in ip_network


def check_ip_match_the_masks(ip, masks):
    for mask in masks:
        if check_ip_match_the_mask(ip, mask):
            return True