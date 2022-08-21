import asyncio
import datetime
import json
import random

import websockets

import csgo

CONNECTIONS = set()


async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def read_mem():
    offset = csgo.read_json()
    pm, client, engine = csgo.get_process()

    while True:
        players, mapname = csgo.read_pos(pm, client, engine, offset)
        #print(mapname)

        if len(players) > 0 and mapname != '':
            data = {}
            data['map'] = mapname
            data['player_list'] = players
            msg = json.dumps(data)
            websockets.broadcast(CONNECTIONS, msg)
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(register, "0.0.0.0", 9999):
        await read_mem()


if __name__ == "__main__":
    asyncio.run(main())
