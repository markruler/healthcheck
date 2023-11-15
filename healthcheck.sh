#!/usr/bin/env bash

# 기본 retry 횟수
RETRY_COUNT=1

# 사용법 메시지 출력 함수
usage() {
  echo "Usage: $0 [-u <URL>] [-r <retry_count>]"
  echo "Options:"
  echo "  -u <URL>: Health check할 대상 URL"
  echo "  -r <retry_count>: Health check 재시도 횟수 (기본값: $RETRY_COUNT)"
  exit 1
}

# 명령행 옵션 파싱
while getopts "u:r:" opt; do
  case $opt in
  u)
    HEALTH_CHECK_URL="$OPTARG"
    ;;
  r)
    RETRY_COUNT="$OPTARG"
    ;;
  \?)
    usage
    ;;
  esac
done

# Health check 함수 정의
check_health() {
  for ((i = 1; i <= $RETRY_COUNT; i++)); do
    # --fail: Fail silently (no output at all) on HTTP errors (-f)
    # --silent: Silent or quiet mode (-s)
    # --location: Follow redirects (-L)
    # --write-out: Use output FORMAT after completion
    # --max-time: Maximum time(in seconds) allowed for the transfer
    response_code=$(curl \
                      --header "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36" \
                      --silent \
                      --location \
                      --output /dev/null \
                      --fail \
                      --write-out "%{http_code}" \
                      --max-time 5 \
                      $HEALTH_CHECK_URL)

    if [ $response_code -eq 200 ]; then
      echo "Health check: OK (HTTP $response_code)"
      exit 0
    else
      echo "Retry $i: Health check failed (HTTP $response_code)"
    fi

    if [ $i -lt $RETRY_COUNT ]; then
      sleep 5 # 재시도 사이에 5초 대기
    fi
  done

  echo "Health check: Failed after $RETRY_COUNT retries"
  exit 1
}

# Health check 실행
check_health
