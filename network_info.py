import ipaddress
import platform
import socket
import subprocess


def get_hostname():
    """Return the computer's hostname."""
    return socket.gethostname()


def get_operating_system():
    """Return the operating system name."""
    return f"{platform.system()} {platform.release()}"


def get_local_ip():
    """
    Find the local IPv4 address used by the computer.

    This does not send data to the internet.
    It only asks the operating system which network
    interface would be used for a connection.
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        connection.connect(("8.8.8.8", 80))
        local_ip = connection.getsockname()[0]
        return local_ip

    except OSError:
        return "Not detected"

    finally:
        connection.close()


def get_default_gateway():
    """
    Find the default gateway on Linux using the `ip route` command.
    """
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True,
            text=True,
            check=False,
        )

        output = result.stdout.strip()

        if not output:
            return "Not detected"

        parts = output.split()

        if "via" in parts:
            gateway_index = parts.index("via") + 1
            return parts[gateway_index]

        return "Not detected"

    except (OSError, IndexError):
        return "Not detected"


def get_network_range(local_ip):
    """
    Calculate the local /24 network range.

    Example:
    Local IP: 192.168.1.15
    Network:  192.168.1.0/24
    """
    if local_ip == "Not detected":
        return "Not detected"

    try:
        network = ipaddress.ip_network(
            f"{local_ip}/24",
            strict=False,
        )
        return str(network)

    except ValueError:
        return "Not detected"


def get_network_info():
    """Collect all network and system information."""
    local_ip = get_local_ip()

    return {
        "hostname": get_hostname(),
        "operating_system": get_operating_system(),
        "local_ip": local_ip,
        "network_range": get_network_range(local_ip),
        "gateway": get_default_gateway(),
    }


if __name__ == "__main__":
    information = get_network_info()

    for key, value in information.items():
        print(f"{key}: {value}")