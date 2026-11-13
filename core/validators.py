
import ipaddress


def valid_port(value):
    """Valida un puerto TCP."""

    try:
        port = int(value)
        return 1 <= port <= 65535
    except (TypeError, ValueError):
        return False


def valid_ip(value):
    """Valida una dirección IP sin puerto."""

    try:
        ipaddress.ip_address(value.strip())
        return True
    except (AttributeError, ValueError):
        return False
