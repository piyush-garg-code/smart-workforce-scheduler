"""Command-line client for the local scheduler service."""

import argparse
import json
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description="Smart Workforce Scheduler")
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    parser.add_argument("--workers", nargs="+")
    parser.add_argument("--worker")
    parser.add_argument("--analytics", action="store_true")
    args = parser.parse_args()
    if args.workers:
        request = Request(
            args.url + "/api/schedules",
            data=json.dumps({"workers": args.workers}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
    else:
        path = "/api/analytics" if args.analytics else "/api/schedules"
        if args.worker:
            path += "?worker=" + args.worker
        request = Request(args.url + path)
    with urlopen(request) as response:
        print(json.dumps(json.loads(response.read()), indent=2))


if __name__ == "__main__":
    main()
