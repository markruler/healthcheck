#!/usr/bin/env python3

import json
import time

import requests

"""_summary_
python3 healthcheck.py --url https://www.python.org --retry 3
"""


def healthcheck(
        url: str,
        retry: int,
):
    for count in range(retry):
        print(f"({count + 1}/{retry}) Healthchecking... {url}")
        if count > 0:
            # 재시도 대기 3초
            time.sleep(3)

        try:
            # 요청 대기 3초
            response = requests.get(
                url=url,
                timeout=3,
                allow_redirects=True,
                headers={
                    # to avoid `tarpit`
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
                },
            )

            print(f"response.status_code: {response.status_code}")
            if response.status_code == 200:
                break
            elif response.text == 'OK':
                print(f"response.text: {response.text}")
                break
            elif response.json()['status'] == 'UP':
                # Spring Actuator
                print(f"response.json(): {response.json()['status']}")
                break
            else:
                check_retry_limit(count, retry)
                continue
        except json.decoder.JSONDecodeError as ex:
            print(ex.__class__, ex)
            print(f"response.status_code: {response.status_code}")
            continue
        except Exception as ex:
            # print(dir(ex))
            print(ex.__class__, ex)
            continue
        finally:
            check_retry_limit(count, retry)


def check_retry_limit(count, retry):
    if count == (retry - 1):
        print("Retry count exceeded")
        exit(1)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Simple Healthcheck Tool")
    parser.add_argument(
        "-u", "--url",
        type=str,
        required=True,
        help="Target URL"
    )
    parser.add_argument(
        "-r", "--retry",
        type=int,
        required=False,
        default=1,
        help="Retry count"
    )

    args = parser.parse_args()
    healthcheck(args.url, args.retry)
