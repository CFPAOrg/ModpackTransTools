import collections
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

    "pro": "properties:10",  # 无用固定字段
    "bq": "betterquesting:10",  # 无用固定字段
    "name": "name:8",  # 具体任务的名称
    "desc": "desc:8"  # 具体任务的描述
}

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

    # 将 json 文件构建为语言文件，格式如下
    # "db.0:10.3.name": "xxxxxxxxxxxx"
    # "line.2:10.2.desc": "xxxxxxxxxxxxx"
    DATABASE = {}  # 顾名思义，存储所有任务
    INDEX = {}  # 存储章节对应任务的
    OUT = collections.OrderedDict()  # 有序词典，最后输出语言文件用的

    # 将所有任务部分语言文件分离出来
    for k, v in MAIN[KEY.get('db')].items():
        DATABASE['db.{}.name'.format(str(v[KEY.get('qid')]))] = v[KEY.get('pro')][
            KEY.get('bq')][KEY.get('name')]
        DATABASE['db.{}.desc'.format(str(v[KEY.get('qid')]))] = v[KEY.get('pro')][
            KEY.get('bq')][KEY.get('desc')].lstrip()

    # 将所有的章节对应任务映射表提取出来
    for k, v in MAIN[KEY.get('line')].items():
        INDEX[k] = [i[KEY.get('id')] for i in v[KEY.get('q')].values()]

    # 开始有序理出章节对应任务
    for k, v in INDEX.items():
        # 存储章节标题和描述
        OUT['line.{}.name'.format(str(k[:-3]))] = MAIN[KEY.get('line')][k][
            KEY.get('pro')][KEY.get('bq')][KEY.get('name')]
        OUT['line.{}.desc'.format(str(k[:-3]))] = MAIN[KEY.get('line')][k][
            KEY.get('pro')][KEY.get('bq')][KEY.get('desc')].lstrip()

        # 存储具体任务
        # 因为一些原因，可能会存在章节中存有不存在的任务 ID，必须要进行校验
        for i in v:
            if 'db.{}.name'.format(str(i)) in DATABASE:
                OUT['db.{}.name'.format(str(i))] = DATABASE['db.{}.name'.format(str(i))]
            if 'db.{}.desc'.format(str(i)) in DATABASE:
                OUT['db.{}.desc'.format(str(i))] = DATABASE['db.{}.desc'.format(str(i))]

    # 输出成文件
    with open('zh_cn.json', 'w', encoding='utf-8') as w:
        json.dump(OUT, w, ensure_ascii=False, indent=2, separators=(',', ': '))
