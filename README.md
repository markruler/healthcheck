# Healthcheck

## Python

```sh
# chmod +x healthcheck.py
# python3 healthcheck.py --url https://www.python.org --retry 3
./healthcheck.py -u https://www.python.org -r 3
```

Jenkins 등의 CI 도구에서 console output을 실시간으로 확인하고 싶다면
[PYTHONUNBUFFERED=x](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED) 옵션을 추가한다.

## Shell Script

```sh
# chmod +x healthcheck.sh
./healthcheck.sh -u https://curl.se -r 3
```

## JavaScript

```sh
# chmod +x healthcheck.js
# npm install --save=false yargs
./healthcheck.js -u https://nodejs.org -r 3
```
