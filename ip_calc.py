"""
Parse raw IP address
"""


def ip_to_int(ip_address: str) -> int | None:
    """
    Converts string IP address to int

    Parameters
    ----------
    ip : str
        IP address in a format of xxx.xxx.xxx.xxx

    Returns
    -------
    int
        IP address in a format of int

    None
        If IP address is not valid

    Doctests
    --------
    >>> ip_to_int("192.168.0.1")
    3232235521
    >>> ip_to_int("192.168.0.256")
    >>> ip_to_int("192.168.0")
    >>> ip_to_int("127.0.0.1")
    2130706433
    >>> ip_to_int("test")
    >>> ip_to_int(2130706433)
    >>> ip_to_int("12.2.2")
    >>> ip_to_int("912.44.2.2")
    >>> ip_to_int("255.255.255.255")
    4294967295
    """
    if not isinstance(ip_address, str):
        return None
    if not ip_address.count(".") == 3:
        return None
    if not all(i.isdigit() for i in ip_address.split(".")):
        return None
    if not all(0 <= int(i) <= 255 for i in ip_address.split(".")):
        return None
    return int("".join(f"{str(bin(int(i)))[2:]:0>8}" for i in ip_address.split(".")), 2)

def int_to_ip(ip_address: int) -> str | None:
    """
    Converts int IP address to string

    Parameters
    ----------
    ip : int
        IP address in a format of int

    Returns
    -------
    str
        IP address in a format of xxx.xxx.xxx.xxx

    None
        If IP address is not valid

    Doctests
    --------
    >>> int_to_ip(3232235521)
    '192.168.0.1'
    >>> int_to_ip(2130706433)
    '127.0.0.1'
    >>> int_to_ip(4294967295)
    '255.255.255.255'
    >>> int_to_ip(4294967296)
    >>> int_to_ip(-1)
    >>> int_to_ip("test")
    >>> int_to_ip(2130706433.0)
    """
    if not isinstance(ip_address, int):
        return None
    if not 0 <= ip_address <= 4294967295:
        return None
    bin_str_ip = f"{str(bin(ip_address))[2:]:0>32}"
    return ".".join(
        str(int(bin_str_ip[i : i + 8], 2))
        for i in range(0, len(bin_str_ip), 8))

def validate_raw_address(raw_address: str) -> bool:
    """
    Check if raw IP address is valid

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    bool
        True if raw IP address is valid, False otherwise

    Doctests
    --------
    >>> validate_raw_address("192.168.0.1/16")
    True
    >>> validate_raw_address("192.168.0.1/32")
    True
    >>> validate_raw_address("192.168.0.1/33")
    False
    >>> validate_raw_address("192.268.0.1/16")
    False
    >>> validate_raw_address("-2.4.4.1/16")
    False
    >>> validate_raw_address("test")
    False
    >>> validate_raw_address("2.2.2.2/2/2")
    False
    >>> validate_raw_address("2.2.2/2")
    False
    """
    if not isinstance(raw_address, str):
        return False
    if not "/" in raw_address:
        return False
    if len(raw_address.split("/")) != 2:
        return False
    if not raw_address.split("/")[0].count(".") == 3:
        return False
    if not all(i.isdigit() for i in raw_address.split("/")[0].split(".")):
        return False
    if not all(0 <= int(i) <= 255 for i in raw_address.split("/")[0].split(".")):
        return False
    if not raw_address.split("/")[1].isdigit():
        return False
    if not 0 <= int(raw_address.split("/")[1]) <= 32:
        return False
    return True

def get_ip_from_raw_address(raw_address: str) -> str | None:
    """
    Get IP address from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        IP address in a format of xxx.xxx.xxx.xxx

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_ip_from_raw_address("192.168.0.1/16")
    '192.168.0.1'
    >>> get_ip_from_raw_address("192.168.0.1/33")
    >>> get_ip_from_raw_address("192.268.0.1/16")
    >>> get_ip_from_raw_address("-192.168.0.1/16")
    >>> get_ip_from_raw_address("test")
    >>> get_ip_from_raw_address("127.0.0.1/2/2")
    >>> get_ip_from_raw_address("127.0.0/2")
    >>> get_ip_from_raw_address("127.0.0.1/2")
    '127.0.0.1'
    """
    if not validate_raw_address(raw_address):
        return None
    return raw_address.split('/')[0]

def get_network_address_from_raw_address(raw_address: str) -> str | None:
    """
    Get network address from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        Network address in a format of xxx.xxx.xxx.xxx

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_network_address_from_raw_address("192.168.0.1/16")
    '192.168.0.0'
    >>> get_network_address_from_raw_address("192.168.0.1/33")
    >>> get_network_address_from_raw_address("192.268.0.1/16")
    >>> get_network_address_from_raw_address("-192.168.0.1/16")
    >>> get_network_address_from_raw_address("test")
    >>> get_network_address_from_raw_address("127.0.0.1/2/2")
    >>> get_network_address_from_raw_address("127.0.0/2")
    >>> get_network_address_from_raw_address("127.0.1.1/24")
    '127.0.1.0'
    """
    if not validate_raw_address(raw_address):
        return None
    binary_mask_str = get_binary_mask_from_raw_address(raw_address)
    ip_str = get_ip_from_raw_address(raw_address)
    if binary_mask_str is None or ip_str is None:
        return None
    mask = int(binary_mask_str.replace(".", ""), 2)
    ip_address = ip_to_int(ip_str)
    if ip_address is None:
        return None
    binary_network_address = ip_address & mask
    return int_to_ip(binary_network_address)

def get_broadcast_address_from_raw_address(raw_address: str) -> str | None:
    """
    Get broadcast address from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        Broadcast address in a format of xxx.xxx.xxx.xxx

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_broadcast_address_from_raw_address("192.168.0.1/16")
    '192.168.255.255'
    >>> get_broadcast_address_from_raw_address("192.168.0.1/33")
    >>> get_broadcast_address_from_raw_address("192.268.0.1/16")
    >>> get_broadcast_address_from_raw_address("-192.168.0.1/16")
    >>> get_broadcast_address_from_raw_address("test")
    >>> get_broadcast_address_from_raw_address("127.0.0.1/2/2")
    >>> get_broadcast_address_from_raw_address("127.0.0/2")
    >>> get_broadcast_address_from_raw_address("127.0.1.1/24")
    '127.0.1.255'
    """
    if not validate_raw_address(raw_address):
        return None
    binary_mask_str = get_binary_mask_from_raw_address(raw_address)
    ip_str = get_ip_from_raw_address(raw_address)
    if binary_mask_str is None or ip_str is None:
        return None
    binary_mask_str = binary_mask_str.replace(".", "")
    inverted_binary_mask_str = "".join("1" if i == "0" else "0" for i in binary_mask_str)
    ip_address = ip_to_int(ip_str)
    mask = int(inverted_binary_mask_str, 2)
    if ip_address is None:
        return None
    binary_broadcast_address = ip_address | mask
    return int_to_ip(binary_broadcast_address)

def get_binary_mask_from_raw_address(raw_address: str) -> str | None:
    """
    Get binary mask from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        The mask in a binary format

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_binary_mask_from_raw_address("192.168.0.1/16")
    '11111111.11111111.00000000.00000000'
    >>> get_binary_mask_from_raw_address("192.168.0.1/33")
    >>> get_binary_mask_from_raw_address("192.268.0.1/16")
    >>> get_binary_mask_from_raw_address("-192.168.0.1/16")
    >>> get_binary_mask_from_raw_address("test")
    >>> get_binary_mask_from_raw_address("127.0.0.1/2/2")
    >>> get_binary_mask_from_raw_address("127.0.0/2")
    >>> get_binary_mask_from_raw_address("127.0.1.1/24")
    '11111111.11111111.11111111.00000000'
    """
    if not validate_raw_address(raw_address):
        return None
    subnet = int(raw_address.split("/")[1])
    mask = "1" * subnet + "0" * (32 - subnet)
    return ".".join(mask[i : i + 8] for i in range(0, len(mask), 8))

def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str | None:
    """
    Get first usable IP address from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        First usable IP address in a format of xxx.xxx.xxx.xxx

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_first_usable_ip_address_from_raw_address("192.168.0.1/16")
    '192.168.0.1'
    >>> get_first_usable_ip_address_from_raw_address("192.168.0.1/33")
    >>> get_first_usable_ip_address_from_raw_address("192.268.0.1/16")
    >>> get_first_usable_ip_address_from_raw_address("-192.168.0.1/16")
    >>> get_first_usable_ip_address_from_raw_address("test")
    >>> get_first_usable_ip_address_from_raw_address("127.0.0.1/2/2")
    >>> get_first_usable_ip_address_from_raw_address("127.0.0/2")
    >>> get_first_usable_ip_address_from_raw_address("127.0.1.1/24")
    '127.0.1.1'
    """
    if not validate_raw_address(raw_address):
        return None
    network_address = get_network_address_from_raw_address(raw_address)
    if network_address is None:
        return None
    int_network_address = ip_to_int(network_address)
    if int_network_address is None:
        return None
    return int_to_ip(int_network_address + 1)

def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str | None:
    """
    Get penultimate IP address from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        Penultimate IP address in a format of xxx.xxx.xxx.xxx

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_penultimate_usable_ip_address_from_raw_address("192.168.0.1/16")
    '192.168.255.253'
    >>> get_penultimate_usable_ip_address_from_raw_address("192.168.0.1/33")
    >>> get_penultimate_usable_ip_address_from_raw_address("192.268.0.1/16")
    >>> get_penultimate_usable_ip_address_from_raw_address("-192.168.0.1/16")
    >>> get_penultimate_usable_ip_address_from_raw_address("test")
    >>> get_penultimate_usable_ip_address_from_raw_address("127.0.0.1/2/2")
    >>> get_penultimate_usable_ip_address_from_raw_address("127.0.0/2")
    >>> get_penultimate_usable_ip_address_from_raw_address("127.0.1.1/24")
    '127.0.1.253'
    """
    if not validate_raw_address(raw_address):
        return None
    broadcast_address = get_broadcast_address_from_raw_address(raw_address)
    if broadcast_address is None:
        return None
    int_broadcast_address = ip_to_int(broadcast_address)
    if int_broadcast_address is None:
        return None
    return int_to_ip(int_broadcast_address - 2)

def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> int | None:
    """
    Get number of usable hosts from raw IP address

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    int
        Number of usable hosts

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_number_of_usable_hosts_from_raw_address("192.168.0.1/16")
    65534
    >>> get_number_of_usable_hosts_from_raw_address("192.168.0.1/33")
    >>> get_number_of_usable_hosts_from_raw_address("192.268.0.1/16")
    >>> get_number_of_usable_hosts_from_raw_address("-192.168.0.1/16")
    >>> get_number_of_usable_hosts_from_raw_address("test")
    >>> get_number_of_usable_hosts_from_raw_address("127.0.0.1/2/2")
    >>> get_number_of_usable_hosts_from_raw_address("127.0.0/2")
    >>> get_number_of_usable_hosts_from_raw_address("127.0.1.1/24")
    254
    """
    if not validate_raw_address(raw_address):
        return None
    return 2 ** (32 - int(raw_address.split("/")[1])) - 2

def get_ip_class_from_raw_address(raw_address: str) -> str | None:
    """
    Get IP class from raw IP address

    Parameters
    ----------

    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    str
        IP class

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> get_ip_class_from_raw_address("192.168.0.1/24")
    'C'
    >>> get_ip_class_from_raw_address("127.0.0.1/24")
    >>> get_ip_class_from_raw_address("98.2.4.1/12")
    'A'
    >>> get_ip_class_from_raw_address("130.4.2.2/16")
    'B'
    >>> get_ip_class_from_raw_address("210.4.3.1/24")
    'C'
    >>> get_ip_class_from_raw_address("220.3.5.5/32")
    'C'
    >>> get_ip_class_from_raw_address("240.4.4.4/32")
    'E'
    >>> get_ip_class_from_raw_address("256.4.4.4/32")
    >>> get_ip_class_from_raw_address("-256.4.4.4/32")
    >>> get_ip_class_from_raw_address("test")
    >>> get_ip_class_from_raw_address("4.4.4/4")
    >>> get_ip_class_from_raw_address("4.4.4.4/4/4")
    """
    if not validate_raw_address(raw_address):
        return None
    ip_address = get_ip_from_raw_address(raw_address)
    if ip_address is None:
        return None
    ip_int = ip_to_int(ip_address)
    if ip_int is None:
        return None
    a_start = ip_to_int("1.0.0.0")
    a_end = ip_to_int("126.255.255.255")
    b_start = ip_to_int("128.0.0.0")
    b_end = ip_to_int("191.255.255.255")
    c_start = ip_to_int("192.0.0.0")
    c_end = ip_to_int("223.255.255.255")
    d_start = ip_to_int("224.0.0.0")
    d_end = ip_to_int("239.255.255.255")
    e_start = ip_to_int("240.0.0.0")
    e_end = ip_to_int("255.255.255.255")
    if a_start is None or a_end is None:
        return None
    if b_start is None or b_end is None:
        return None
    if c_start is None or c_end is None:
        return None
    if d_start is None or d_end is None:
        return None
    if e_start is None or e_end is None:
        return None
    if a_start <= ip_int <= a_end:
        return "A"
    if b_start <= ip_int <= b_end:
        return "B"
    if c_start <= ip_int <= c_end:
        return "C"
    if d_start <= ip_int <= d_end:
        return "D"
    if e_start <= ip_int <= e_end:
        return "E"
    return None

def check_private_ip_address_from_raw_address(raw_address: str) -> bool | None:
    """
    Check if IP address is private

    Parameters
    ----------
    raw_address : str
        Raw IP address in a format of xxx.xxx.xxx.xxx/xx

    Returns
    -------
    bool
        True if IP address is private, False otherwise

    None
        If raw IP address is not valid

    Doctests
    --------
    >>> check_private_ip_address_from_raw_address("192.168.0.1/24")
    True
    >>> check_private_ip_address_from_raw_address("127.0.0.1/12")
    False
    >>> check_private_ip_address_from_raw_address("10.0.0.1/24")
    True
    >>> check_private_ip_address_from_raw_address("172.16.0.4/24")
    True
    >>> check_private_ip_address_from_raw_address("14.0.0.1/24")
    False
    >>> check_private_ip_address_from_raw_address("256.4.4.4/32")
    >>> check_private_ip_address_from_raw_address("-256.4.4.4/32")
    >>> check_private_ip_address_from_raw_address("test")
    >>> check_private_ip_address_from_raw_address("4.4.4/4")
    >>> check_private_ip_address_from_raw_address("4.4.4.4/4/4")
    """
    if not validate_raw_address(raw_address):
        return None
    ip_address = get_ip_from_raw_address(raw_address)
    if ip_address is None:
        return None
    if ip_address.split(".")[0] == "10":
        return True
    if ip_address.split(".")[0] == "172" and 16 <= int(ip_address.split(".")[1]) <= 31:
        return True
    if ip_address.split(".")[0] == "192" and ip_address.split(".")[1] == "168":
        return True
    return False


if __name__ == "__main__":
    # import doctest
    # print(doctest.testmod())
    ip = input()
    if not validate_raw_address(ip):
        if "/" not in ip and ip_to_int(ip) is not None:
            print("Missing prefix")
            exit()
        print("Error")
        exit()
    print(f"IP address: {get_ip_from_raw_address(ip)}")
    print(f"Network Address: {get_network_address_from_raw_address(ip)}")
    print(f"Broadcast Address: {get_broadcast_address_from_raw_address(ip)}")
    print(f"Binary Subnet Mask: {get_binary_mask_from_raw_address(ip)}")
    print(f"First usable host IP: {get_first_usable_ip_address_from_raw_address(ip)}")
    print(f"Penultimate usable host IP: {get_penultimate_usable_ip_address_from_raw_address(ip)}")
    print(f"Number of usable Hosts: {get_number_of_usable_hosts_from_raw_address(ip)}")
    print(f"IP class: {get_ip_class_from_raw_address(ip)}")
    print(f"IP type private: {check_private_ip_address_from_raw_address(ip)}")
