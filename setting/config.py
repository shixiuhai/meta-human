
import configparser
import json
import os.path
import sys
sys.path.append("..")

file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')

_config = configparser.RawConfigParser()
_config.read(file_path)

tss_settings = dict(_config.items('tss'))


action_plugin = _config.getboolean('human-model', 'action')
schedule_plugin = _config.getboolean('human-model', 'schedule')
speech_plugin = _config.getboolean('human-model', 'speech')

try:
    live2D_actions = []
    live2D_embeddings = []
    if action_plugin:
        with open("./action.json", 'r') as load_f:
            live2D_action_dict = json.load(load_f)
        live2D_actions = live2D_action_dict.keys()
        live2D_embeddings = [live2D_action_dict[action] for action in live2D_actions]
except Exception as e:
    print('读取embedding文件错误,请检查是否初始化action,使用action plugin请先运行 python main action', e)

if __name__ == '__main__':
    print(tss_settings)