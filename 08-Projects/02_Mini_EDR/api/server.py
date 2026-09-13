from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

EVENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "logs",
    "events.json"
)

INCIDENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "logs",
    "incidents.json"
)


def load_json_file(file_path):
    """Load JSON data from a file."""

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []

    return []


class EDRRequestHandler(BaseHTTPRequestHandler):

    def send_json(self, data):
        """Send a JSON response."""

        response = json.dumps(
            data
        ).encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(
            response
        )

    def do_GET(self):

        if self.path == "/api/events":

            events = load_json_file(
                EVENTS_FILE
            )

            self.send_json(
                events
            )

            return


        if self.path == "/api/incidents":

            incidents = load_json_file(
                INCIDENTS_FILE
            )

            self.send_json(
                incidents
            )

            return


        if self.path == "/api/status":

            self.send_json({
                "status": "active",
                "service": "Mini EDR API"
            })

            return


        self.send_response(404)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            b'{"error":"Endpoint not found"}'
        )


def main():

    server = HTTPServer(
        ("localhost", 8000),
        EDRRequestHandler
    )

    print(
        "[API] Mini EDR API started"
    )

    print(
        "[API] http://localhost:8000"
    )

    print(
        "[API] Endpoints:"
    )

    print(
        "      /api/events"
    )

    print(
        "      /api/incidents"
    )

    print(
        "      /api/status"
    )

    server.serve_forever()


if __name__ == "__main__":
    main()