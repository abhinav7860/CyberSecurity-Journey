# monitor/network_monitor.py

import psutil


def get_network_connections():
    """Get useful current network connections."""

    connections = []

    for connection in psutil.net_connections(
        kind="inet"
    ):

        try:

            if connection.pid is None:
                continue

            if connection.pid == 0:
                continue

            if not connection.laddr:
                continue

            local_ip = connection.laddr.ip
            local_port = connection.laddr.port

            remote_ip = ""
            remote_port = ""

            if connection.raddr:
                remote_ip = connection.raddr.ip
                remote_port = connection.raddr.port

            if (
                not remote_ip
                and connection.status != "LISTEN"
            ):
                continue

            process_name = "Unknown"

            try:

                process = psutil.Process(
                    connection.pid
                )

                process_name = process.name()

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                pass

            connections.append({
                "pid": connection.pid,
                "process": process_name,
                "local_ip": local_ip,
                "local_port": local_port,
                "remote_ip": remote_ip,
                "remote_port": remote_port,
                "status": connection.status
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return connections