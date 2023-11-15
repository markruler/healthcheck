#!/usr/bin/env python3

import requests
import json
"""_summary_
python3 healthcheck.py --url https://www.python.org --retry 3
"""

def healthcheck(
    url: str,
    retry: int,
):
    for _ in range(retry):
        response = requests.get(
            url=url,
            timeout=3,
            allow_redirects=True,
            headers={
                # to avoid `tarpit`
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
            },
        )

        try:
            if response.status_code == 200:
                print(f"response.status_code: {response.status_code}")
                break
            elif response.text == 'OK':
                print(f"response.text: {response.text}")
                break
            elif response.json()['status'] == 'UP':
                # Spring Actuator
                print(f"response.json(): {response.json()['status']}")
                break
            else:
                continue
        except json.decoder.JSONDecodeError as e:
            print(e.__class__, e)
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Simple Healthcheck Tool")
    parser.add_argument("--url", type=str, required=True, help="Target URL")
    parser.add_argument("--retry", type=int, required=False, default=1, help="Retry count")
    
    args = parser.parse_args()
    healthcheck(args.url, args.retry)
