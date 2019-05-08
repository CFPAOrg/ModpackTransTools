import json
import logging

# 枚举类型，用来映射 json 的 key
KEY = {
    "v": "format:8",  # 此 key 为手册的版本信息

    "db": "questDatabase:9",  # 存储所有具体任务
    "qid": "questID:3",  # 任务 ID（作为识别和后面章节划分用的）

    "line": "questLines:9",  # 存储所有的章节
    "q": "quests:9",  # 具体的章节
    "id": "id:3",  # 章节关联的任务 ID
    "lid": "lineID:3",  # 章节 ID

    "pro": "properties:10",  # 无用固定字段
    "bq": "betterquesting:10",  # 无用固定字段
    "name": "name:8",  # 具体任务的名称
    "desc": "desc:8"  # 具体任务的描述
}


def replace_trans(list_in, index, trans, is_db=True, is_name=True):
    key_1 = KEY.get('db') if is_db else KEY.get('line')
    key_2 = KEY.get('qid') if is_db else KEY.get('lid')

    for rtk, rtv in list_in[key_1].items():
        if rtv[key_2] == index:
            if is_name:
                list_in[key_1][rtk][KEY.get('pro')][KEY.get('bq')][KEY.get('name')] = trans
            else:
                list_in[key_1][rtk][KEY.get('pro')][KEY.get('bq')][KEY.get('desc')] = trans
            break
    return list_in


if __name__ == '__main__':
    # 日志初始化，格式如下
    # [14:28:47] [WARN] 这是一条日志输出信息
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S')

    # 读取 json 文件
    with open('DefaultQuests.json', 'r', encoding='utf-8') as f:
        MAIN = json.load(f)
        logging.debug("DefaultQuests.json 文件已经读取")

    # 读取语言文件
    with open('zh_cn.json', 'r', encoding='utf-8') as f:
        LANG = json.load(f)
        logging.debug("zh_cn.json 文件已经读取")

    # 开始读取 key，进行判断替换
    for k, v in LANG.items():
        i = k[3:-5] if k.startswith('db') else k[5:-5]
        MAIN = replace_trans(MAIN, int(i), k.startswith('db'), k.endswith('name'))

    with open('out.json', 'w', encoding='utf-8') as w:
        json.dump(MAIN, w, ensure_ascii=False, indent=2, separators=(',', ': '))
