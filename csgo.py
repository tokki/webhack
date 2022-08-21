import json
import sys

import pymem


def read_json():
    #steal from https://github.com/frk1/hazedumper/blob/master/csgo.json
    f = open('offset.json', 'r')
    text = ""
    try:
        text = f.read()
    except:
        print("could not find offset.json")
    obj = json.loads(text)
    return obj


def get_process():
    try:
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle,
                                                "client.dll").lpBaseOfDll

        engine = pymem.process.module_from_name(pm.process_handle,
                                                "engine.dll").lpBaseOfDll
    except Exception:
        print("could not find csgo.exe")
        sys.exit()
    return pm, client, engine


def read_pos(pm, client, engine, offset):

    dwEntityList = offset['signatures']['dwEntityList']
    dwLocalPlayer = offset['signatures']['dwLocalPlayer']
    m_iTeamNum = offset['netvars']['m_iTeamNum']
    m_iHealth = offset['netvars']['m_iHealth']
    m_vecOrigin = offset['netvars']['m_vecOrigin']

    dwClientState = offset['signatures']['dwClientState']
    dwClientState_Map = offset['signatures']['dwClientState_Map']

    EntityDist = 16
    players = []
    mapname = ''

    if pm.read_uint(client + dwLocalPlayer):
        state = pm.read_uint(engine + dwClientState)
        mapname = pm.read_string(state + dwClientState_Map)

        localplayer = pm.read_uint(client + dwLocalPlayer)
        localplayer_team = pm.read_uint(localplayer + m_iTeamNum)

        for i in range(1, 64):
            if pm.read_uint(client + dwEntityList + i * EntityDist):
                entity = pm.read_uint(client + dwEntityList + i * EntityDist)

                team_id = pm.read_uint(entity + m_iTeamNum)
                health = pm.read_uint(entity + m_iHealth)
                x = pm.read_float(entity + m_vecOrigin)
                y = pm.read_float(entity + m_vecOrigin + 4)
                if localplayer_team != team_id:
                    player = {}
                    player['health'] = health
                    player['pos_x'] = x
                    player['pos_y'] = y
                    players.append(player)

    return players, mapname
