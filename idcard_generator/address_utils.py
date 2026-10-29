import json
import os
import secrets
secure_random = secrets.SystemRandom()
import sys
from . import utils

_CACHED_ADDRESSES = None

def get_random_address():
    """从配置文件中随机获取一个地址"""
    global _CACHED_ADDRESSES
    if _CACHED_ADDRESSES is not None:
        if _CACHED_ADDRESSES:
            return secure_random.choice(_CACHED_ADDRESSES)
        else:
            return "江苏省南京市鼓楼区中山路1号"

    # 判断是否为打包后的exe环境
    if getattr(sys, 'frozen', False):
        # 打包后的exe环境，从exe同目录读取配置文件
        exe_dir = os.path.dirname(sys.executable)
        config_path = os.path.join(exe_dir, 'address_config.json')
    else:
        # 开发环境，使用原路径
        config_path = os.path.join(utils.get_base_path(), 'idcard_generator', 'address_config.json')
    
    # 如果配置文件不存在，创建默认配置文件
    if not os.path.exists(config_path):
        create_default_config_file(config_path)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            _CACHED_ADDRESSES = config.get('addresses', [])
            if _CACHED_ADDRESSES:
                return secure_random.choice(_CACHED_ADDRESSES)
            else:
                # 如果配置文件为空，返回默认地址
                return "江苏省南京市鼓楼区中山路1号"
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果配置文件不存在或格式错误，返回默认地址
        _CACHED_ADDRESSES = []
        return "江苏省南京市鼓楼区中山路1号"

def create_default_config_file(config_path):
    """创建默认的地址配置文件"""
    default_addresses = [
        "江苏省徐州市云龙区汉山路滨湖花园小区5栋1203室",
        "江苏省徐州市云龙区开元路翠玉新山小区12栋708室",
        "江苏省徐州市云龙区昆仑大道时代艺境小区18栋1615室",
        "江苏省徐州市泉山区学城路公安小区3栋905室",
        "江苏省徐州市泉山区二环西路万通小区7栋1422室",
        "江苏省徐州市泉山区杏花路杏花小区9栋1101室",
        "江苏省徐州市泉山区振兴路振兴工程小区4栋813室",
        "江苏省徐州市鼓楼区北京南路华美商厦小区15栋1704室",
        "江苏省徐州市铜山区金山路天成花园小区2栋506室",
        "江苏省徐州市铜山区苏堤南路泰山汇景花园小区11栋1319室",
        "江苏省徐州市沛县工业路凯旋小区6栋924室",
        "江苏省徐州市云龙区三山路云龙湖小区20栋1002室",
        "江苏省徐州市泉山区段庄街道火花小区8栋1517室",
        "江苏省徐州市贾汪区青年路湖滨小区14栋403室",
        "江苏省徐州市新沂市和平路东都尚城小区16栋1208室",
        "江苏省徐州市丰县前进路丰县花园小区10栋715室",
        "江苏省徐州市邳州市文化路星光小区1栋1105室",
        "江苏省徐州市睢宁县中山路翠岭小区19栋1601室",
        "江苏省徐州市铜山区建国西路大福源小区5栋912室",
        "江苏省徐州市云龙区解放东路府东小区3栋1406室"
    ]
    
    config = {"addresses": default_addresses}
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception:
        # 如果创建失败，忽略错误，程序会使用默认地址
        pass