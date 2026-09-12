import psutil


def get_network_connections():
    """Get useful current network connections."""

    connections = []

    for connection in psutil.net_connections(
        kind="inet"
    ):

        try:

            # Ignore connections without a PID
            if connection.pid is None:
                continue

            # Ignore PID 0
            if connection.pid == 0:
                continue

            # Ignore connections without a local address
            if not connection.laddr:
                continue

            # Get local address
            local_ip = connection.laddr.ip
            local_port = connection.laddr.port

            # Get remote address
            remote_ip = ""
            remote_port = ""

            if connection.raddr:

                remote_ip = connection.raddr.ip
                remote_port = connection.raddr.port

            # Keep LISTEN sockets
            # Keep connections with remote endpoints
            if (
                not remote_ip
                and connection.status != "LISTEN"
            ):
                continue

            # Get process name
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