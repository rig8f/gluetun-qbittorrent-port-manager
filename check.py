import asyncio, os, httpx
# from watchfiles import awatch

PORT_FORWARDED = os.environ["PORT_FORWARDED"]
QB_USER = os.environ["QBITTORRENT_USER"]
QB_PASS = os.environ["QBITTORRENT_PASS"]
QB_SERVER = os.environ["QBITTORRENT_SERVER"]
QB_PORT = os.environ["QBITTORRENT_PORT"]
HTTP_S = os.environ.get("HTTP_S", "http")
SLEEP_TIME_SEC = int(os.environ.get("SLEEP_TIME_SEC", 5))

PREFS_URL = f"{HTTP_S}://{QB_SERVER}:{QB_PORT}/api/v2/app/setPreferences"
LOGIN_URL = f"{HTTP_S}://{QB_SERVER}:{QB_PORT}/api/v2/auth/login"
LOGIN_PAYLOAD = {
    "username": QB_USER,
    "password": QB_PASS,
}


async def update_port(client: httpx.AsyncClient):
    with open(PORT_FORWARDED, 'r', encoding='utf-8') as f:
        port = f.read().strip()

    if 'SID' not in client.cookies:
        await client.post(LOGIN_URL, data=LOGIN_PAYLOAD)

    await client.post(PREFS_URL, data={
        "json": f'{{"listen_port":"{port}"}}'
    })
    print(f"Updated qbittorrent port to {port}")


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        last_mtime = None
        while True:
            if not os.path.exists(PORT_FORWARDED):
                print(f"Couldn't find file {PORT_FORWARDED}")
                print(f"Trying again in {SLEEP_TIME_SEC} seconds")
            else:
                mtime = os.path.getmtime(PORT_FORWARDED)
                if last_mtime is None or mtime != last_mtime:
                    await update_port(client)
                    last_mtime = mtime
            await asyncio.sleep(SLEEP_TIME_SEC)

            # await update_port(client)
            # async for _ in awatch(PORT_FORWARDED):
            #     await update_port(client)


if __name__ == "__main__":
    asyncio.run(main())
