#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import time
"""_summary_
python2 healthcheck_python2.py --url https://www.python.org --retry 3
"""


def healthcheck(
    url,
    retry,
):
    req = urllib2.Request(
        url=url,
        headers={
            # to avoid `tarpit`
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
    )
    for count in range(retry):
        print "(%d/%d) Healthchecking... %s" % (count+1, retry, url)
        if count > 0:
            # 재시도 대기 3초
            time.sleep(3)

        try:
            # 요청 대기 3초
            response = urllib2.urlopen(req, timeout=3)
            if response.code == 200:
                # print dir(response)
                # print response.read()
                print "response.code:", response.code, response.msg
                break
            elif response.read() == 'OK':
                print "response.read():", response.read()
                break
            else:
                check_retry_limit(count, retry)
                continue
        except (urllib2.HTTPError, urllib2.URLError) as ex:
            print ex.__class__, ex.reason
            continue
        except Exception as ex:
            # print dir(ex)
            print ex.__class__, ex
            continue
        finally:
            check_retry_limit(count, retry)


def check_retry_limit(count, retry):
    if count == (retry - 1):
        print "Retry count exceeded"
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
