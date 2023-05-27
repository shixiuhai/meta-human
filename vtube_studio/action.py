import sys
sys.path.append("..")
import asyncio
import pyvts
import json
import random
# https://www.bilibili.com/read/cv22258983/ 语音捕捉
# 基于https://bbs.nga.cn/read.php?tid=28374258&rand=485 语音同步 唇音同步 基础操作
# : ['Heart Eyes', 'Eyes Cry', 'Angry Sign', 'Shock Sign', 'Remove Expressions', 'Anim Shake', '']
from setting.config import live2D_actions

plugin_info = {
    "plugin_name": "start pyvts",
    "developer": "Jiran",
    "authentication_token_path": "./token.txt"
}

async def initialize_action():
    # websocket连接 获取token到本地
    vts = pyvts.vts(plugin_info=plugin_info)
    await vts.connect()
    print('请在live2D VTS弹窗中点击确认!')
    await vts.request_authenticate_token()  # get token
    await vts.write_token()
    await vts.request_authenticate()  # use token

    response_data = await vts.request(vts.vts_request.requestHotKeyList())
    hotkey_list = []
    for hotkey in response_data['data']['availableHotkeys']:
        hotkey_list.append(hotkey['name'])
    print('读取到所有模型动作:', hotkey_list)

    # 请求embedding
    print('请求embedding模型中...')
    # try:
    #     initialize_openai()
    #     res = await openai.Embedding.acreate(input=hotkey_list, model="text-embedding-ada-002")
    #     action_embeddings = [d['embedding'] for d in res['data']]
    #     action_dict = dict(zip(hotkey_list, action_embeddings))
    #     print(len(action_dict))
    # except Exception as e:
    #     print('很可能是翻墙有问题')
    #     raise e

    # # 写入
    # with open("./action.json", "w") as dump_f:
    #     json.dump(action_dict, dump_f)

    # # 测试
    # assert len(hotkey_list) == len(action_dict.keys())  # vts 和 本地的动作是否一致
    # assert len(hotkey_list) not in (0, 1)  # 动作太少
    # action = random.choice(hotkey_list)
    # print('随机播放动作测试...', action)
    send_hotkey_request = vts.vts_request.requestTriggerHotKey("Angry Sign")
    await vts.request(send_hotkey_request)
    await vts.request(send_hotkey_request)
    await vts.request(send_hotkey_request)
    
    await vts.close()

async def play_action(action_index):
    vts = pyvts.vts(plugin_info=plugin_info)
    await vts.connect()
    await vts.read_token()
    await vts.request_authenticate()  # use token

    if action_index > len(live2D_actions) - 1:
        raise '动作不存在'
    send_hotkey_request = vts.vts_request.requestTriggerHotKey(live2D_actions[action_index])
    await vts.request(send_hotkey_request)
    await vts.close()


if __name__ == "__main__":
    action_embeddings = None  # 获取token不需要运行
    
    # asyncio.run(initialize_action())
    hotkey_list=["a","b"]
    action_embeddings=[1,2]
    d=dict(zip(hotkey_list, action_embeddings))
    print(d)
    # asyncio.run(play_action())
