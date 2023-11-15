#!/usr/bin/env node

// npm install --save=false yargs
const yargs = require("yargs");

const argv = yargs
  .option("u", {
    alias: "url",
    type: "string",
    describe: "Health check할 대상 URL",
  })
  .option("r", {
    alias: "retry",
    type: "number",
    describe: "Health check 재시도 횟수",
  })
  .help().argv;

async function main() {
  const healthCheckURL = argv.url;
  console.log(`Health check: ${healthCheckURL}`);
  if (!healthCheckURL) {
    console.error("Health check할 대상 URL을 지정해야 합니다.");
    return;
  }
  const retryCount = argv.retry || 3;

  await checkHealth(healthCheckURL, retryCount);
}

async function checkHealth(url, retryCount) {
  for (let i = 0; i < retryCount; i++) {
    try {
      const response = await fetch(url, {
        timeout: 3_000,
        headers: {
          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
      });
      if (response.status === 200) {
        console.log(`Health check: OK (HTTP ${response.status})`);
        return;
      } else {
        console.log(
          `Retry ${i + 1}: Health check failed (HTTP ${response.status})`
        );
      }

      if (i < retryCount - 1) {
        await new Promise((resolve) => setTimeout(resolve, 5_000)); // 재시도 사이에 5초 대기
      }
    } catch (error) {
      console.error(
        `Retry ${i + 1}: Health check failed (Error: ${error.message})`
      );
      if (i < retryCount - 1) {
        await new Promise((resolve) => setTimeout(resolve, 5_000)); // 재시도 사이에 5초 대기
      }
    }
  }

  console.log(`Health check: Failed after ${retryCount} retries`);
}

main();
