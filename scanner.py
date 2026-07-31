import ipaddress
import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def is_host_online(ip_address, timeout=1):
    """
    Ping one IP address and return True when it responds.
    """

    operating_system = platform.system().lower()

    if operating_system == "windows":
        command = [
            "ping",
            "-n",
            "1",
            "-w",
            str(timeout * 1000),
            ip_address,
        ]
    else:
        command = [
            "ping",
            "-c",
            "1",
            "-W",
            str(timeout),
            ip_address,
        ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        return result.returncode == 0

    except OSError:
        return False


def get_hostname(ip_address):
    """
    Attempt to find the hostname belonging to an IP address.
    """

    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname

    except (socket.herror, socket.gaierror, OSError):
        return "Unknown"


def check_device(ip_address):
    """
    Check one device and return its information if online.
    """

    if not is_host_online(ip_address):
        return None

    return {
        "status": "Online",
        "ip_address": ip_address,
        "hostname": get_hostname(ip_address),
    }


def scan_network(network_range, max_workers=50):
    """
    Scan all usable addresses inside a local network range.

    Example:
        192.168.1.0/24
    """

    try:
        network = ipaddress.ip_network(
            network_range,
            strict=False,
        )

    except ValueError as error:
        raise ValueError(
            f"Invalid network range: {network_range}"
        ) from error

    devices = []

    ip_addresses = [
        str(ip_address)
        for ip_address in network.hosts()
    ]

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_to_ip = {
            executor.submit(
                check_device,
                ip_address,
            ): ip_address
            for ip_address in ip_addresses
        }

        for future in as_completed(future_to_ip):
            try:
                device = future.result()

                if device is not None:
                    devices.append(device)

            except Exception:
                continue

    devices.sort(
        key=lambda device: ipaddress.ip_address(
            device["ip_address"]
        )
    )

    return devices


if __name__ == "__main__":
    test_network = input(
        "Enter a network range, for example 192.168.1.0/24: "
    ).strip()

    print("\nScanning network...\n")

    try:
        discovered_devices = scan_network(test_network)

        if not discovered_devices:
            print("No online devices were found.")

        else:
            print(
                f"Found {len(discovered_devices)} online device(s):\n"
            )

            for device in discovered_devices:
                print(
                    f'{device["ip_address"]:<16} '
                    f'{device["hostname"]:<30} '
                    f'{device["status"]}'
                )

    except ValueError as error:
        print(error)