import json
from urllib.request import urlopen
import logging

import async_timeout
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .util import decrypt_device_id, encrypt_device_id
from .helper import VoiceControlProcessor, VoiceControlDeviceManager
from .const import ATTR_DEVICE_ACTIONS

_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel(logging.DEBUG)
LOGGER_NAME = 'aligenie'

DOMAIN = 'aligenie'

async def createHandler(hass, entry):
    mode = ['handler']
    try:
        # placelist_url = 'https://open.bot.tmall.com/oauth/api/placelist'
        # aliaslist_url = 'https://open.bot.tmall.com/oauth/api/aliaslist'
        # session = async_get_clientsession(hass, verify_ssl=False)
        # with async_timeout.timeout(5, loop=hass.loop):
        #     response = await session.get(placelist_url)
        # placelist  = (await response.json())['data']
        # with async_timeout.timeout(5, loop=hass.loop):
        #     response = await session.get(aliaslist_url)
        # aliaslist = (await response.json())['data']

        response = {"success":True,"data":["门口","客厅","卧室","客房","主卧","次卧","书房","餐厅","厨房","洗手间","浴室","阳台","宠物房","老人房","儿童房","婴儿房","保姆房","玄关","一楼","二楼","三楼","四楼","楼梯","走廊","过道","楼上","楼下","影音室","娱乐室","工作间","杂物间","衣帽间","吧台","花园","温室","车库","休息室","办公室","起居室"]}
        placelist  = response['data']

        response = {"success":True,"data":[{"key":"除湿机","value":["除湿机","除湿器"]},{"key":"冰箱","value":["冰箱"]},{"key":"风扇","value":["风扇","电风扇","落地扇","电扇","台扇","壁扇","顶扇","驱蚊风扇","暖风扇","净化暖风扇","冷风扇","塔扇"]},{"key":"窗帘","value":["窗帘","窗纱","布帘","纱帘","百叶帘","卷帘"]},{"key":"空气净化器","value":["净化器","空气净化器"]},{"key":"扫地机器人","value":["扫地机器人","扫地机","打扫机","自动打扫机"]},{"key":"加湿器","value":["加湿器","空气加湿器","加湿机","空气加湿机"]},{"key":"空气净化器","value":["空气净化器","空净","空气清洁器"]},{"key":"冰箱","value":["双开门冰箱","冰柜"]},{"key":"温控器","value":["温控器","温控"]},{"key":"地暖","value":["地暖"]},{"key":"洗碗机","value":["洗碗机","洗碗器"]},{"key":"干衣机","value":["干衣机","干衣器"]},{"key":"红外幕帘探测器","value":["幕帘"]},{"key":"声光报警器","value":["声光报警器"]},{"key":"水族箱控制器","value":["智能鱼缸","鱼缸"]},{"key":"电蒸箱","value":["电蒸箱"]},{"key":"遥控器","value":["遥控器"]},{"key":"暖气","value":["暖气","暖气机","电暖","电暖气"]},{"key":"空气清新机","value":["空气清新机"]},{"key":"热水器","value":["热水器","电热水器","燃气热水器"]},{"key":"灯","value":["灯","房灯","吸顶灯","床头灯","床灯","电灯","吊灯","台灯","落地灯","壁灯","挂灯","射灯","筒灯","灯带","灯条","暗藏灯","背景灯","阅读灯","柜灯","衣柜灯","天花灯","路灯","彩灯"]},{"key":"电饭煲","value":["电饭煲","电饭锅","饭煲","饭锅"]},{"key":"烤箱","value":["烤箱","嵌入式烤箱"]},{"key":"摄像头","value":["摄像头","摄像","摄像机"]},{"key":"插座","value":["插座","插头","排插单孔单控"]},{"key":"空气监测仪","value":["空气监测仪","空气检测器"]},{"key":"路由器","value":["路由器","路由","智能路由器"]},{"key":"抽油烟机","value":["抽油烟机","抽烟机","烟机"]},{"key":"饮水机","value":["饮水机"]},{"key":"净水器","value":["净水器；净水机"]},{"key":"晾衣架","value":["晾衣架","衣架","晒衣架"]},{"key":"报警器","value":["报警器"]},{"key":"电压力锅","value":["压力锅","高压锅"]},{"key":"微波炉","value":["微波炉"]},{"key":"取暖器","value":["取暖器","加热器"]},{"key":"电热水壶","value":["养生水壶","水壶","养生壶","热水壶","电水壶"]},{"key":"电热毯","value":["电热毯"]},{"key":"足浴器","value":["足浴器","足浴盆","洗脚盆"]},{"key":"暖灯","value":["暖灯"]},{"key":"浴霸","value":["浴霸"]},{"key":"空气炸锅","value":["空气炸锅"]},{"key":"面包机","value":["面包机"]},{"key":"消毒碗柜","value":["消毒碗柜","消毒柜"]},{"key":"电炖锅","value":["电炖锅","炖锅","慢炖锅"]},{"key":"豆浆机","value":["豆浆机"]},{"key":"血糖仪","value":["血糖仪"]},{"key":"电子秤","value":["电子秤","体重秤"]},{"key":"血压计","value":["血压计","血压器"]},{"key":"按摩仪","value":["按摩仪"]},{"key":"油汀","value":["油汀"]},{"key":"燃气灶","value":["燃气灶"]},{"key":"新风机","value":["新风机"]},{"key":"吸奶器","value":["吸奶器"]},{"key":"婴童煲","value":["婴童煲"]},{"key":"按摩椅","value":["按摩椅"]},{"key":"头带","value":["头带"]},{"key":"手环","value":["手环"]},{"key":"手表","value":["手表","表"]},{"key":"智能门控","value":["智能门锁","门锁","电子锁"]},{"key":"煤气盒子","value":["煤气盒子"]},{"key":"空气盒子","value":["空气盒子"]},{"key":"背景音乐系统","value":["背景音乐系统"]},{"key":"辅食机","value":["辅食机"]},{"key":"烟雾报警器","value":["烟雾报警器"]},{"key":"动感单车","value":["动感单车"]},{"key":"美容喷雾机","value":["美容喷雾机"]},{"key":"冰淇淋机","value":["冰淇淋机"]},{"key":"挂烫机","value":["挂烫机"]},{"key":"箱锁柜锁","value":["箱锁柜锁"]},{"key":"料理棒","value":["料理棒"]},{"key":"心率仪","value":["心率仪"]},{"key":"体温计","value":["体温计"]},{"key":"电饼铛","value":["电饼铛"]},{"key":"智能语音药盒","value":["智能语音药盒"]},{"key":"浴缸","value":["浴缸"]},{"key":"原汁机","value":["原汁机"]},{"key":"破壁机","value":["破壁机","超跑"]},{"key":"入墙开关","value":["单开开关"]},{"key":"保险箱","value":["保险箱"]},{"key":"料理机","value":["料理机"]},{"key":"榨油机","value":["榨油机"]},{"key":"电视盒子","value":["电视盒子","盒子","小米盒子","荣耀盒子","乐视盒子","智能盒子"]},{"key":"网关","value":["网关"]},{"key":"智能音箱","value":["音箱"]},{"key":"暖奶器","value":["暖奶器","热奶器","牛奶","调奶器","温奶器","冲奶机"]},{"key":"咖啡机","value":["咖啡机"]},{"key":"故事机","value":["故事机"]},{"key":"嵌入式电蒸箱","value":["嵌入式电蒸箱"]},{"key":"嵌入式微波炉","value":["嵌入式微波炉"]},{"key":"水浸探测器","value":["水浸探测器"]},{"key":"跑步机","value":["跑步机"]},{"key":"智能牙刷","value":["智能牙刷"]},{"key":"门禁室内机","value":["门禁室内机"]},{"key":"WIFI中继器","value":["WIFI中继器"]},{"key":"种植机","value":["种植机"]},{"key":"美容仪","value":["美容仪"]},{"key":"智能场景开关","value":["智能场景开关"]},{"key":"智能云音箱","value":["音箱"]},{"key":"投影仪","value":["投影仪","投影机","投影","背投"]},{"key":"门磁","value":["门磁"]},{"key":"血糖","value":["血糖仪"]},{"key":"磁感应开关","value":["磁感应开关"]},{"key":"红外探测器","value":["人体检测器","人体检测仪"]},{"key":"报警套件","value":["报警套件"]},{"key":"防丢报警器","value":["防丢报警器"]},{"key":"胎音仪","value":["胎音仪"]},{"key":"净水器","value":["净水器箱型"]},{"key":"洗衣机","value":["顶开式洗衣机","滚筒洗衣机"]},{"key":"足浴盆","value":["足浴盆"]},{"key":"洗脚盆","value":["洗脚盆","脚盆"]},{"key":"衣架","value":["衣架","衣架"]},{"key":"空气检测器","value":["空气检测器"]},{"key":"电饭锅","value":["电饭锅"]},{"key":"空调","value":["空调","空气调节器","挂式空调"]},{"key":"煤气灶","value":["煤气灶","煤气"]},{"key":"吹风机","value":["吹风机","电吹风"]},{"key":"门","value":["门"]},{"key":"烹饪机","value":["烹饪机"]},{"key":"电磁炉","value":["磁炉","电磁炉"]}]}
        aliaslist  = response['data']

        placelist.append({'key': '电视', 'value': ['电视机']})
        aliaslist.append({'key': '传感器', 'value': ['传感器']})
    except:
        placelist = []
        aliaslist = []
        import traceback
        _LOGGER.info("[%s] can get places and aliases data from website, set None.\n%s", LOGGER_NAME, traceback.format_exc())
    return VoiceControlAligenie(hass, mode, entry, placelist, aliaslist)

class PlatformParameter:
    device_attribute_map_h2p = {
        'power_state': 'powerstate',
        'color': 'color',
        'temperature': 'temperature',
        'humidity': 'humidity',
        # '': 'windspeed',
        'brightness': 'brightness',
        # '': 'direction',
        # '': 'angle',
        'pm25': 'pm2.5',
    }
    device_action_map_h2p ={
        'turn_on': 'TurnOn',
        'turn_off': 'TurnOff',
        'increase_brightness': 'AdjustUpBrightness',
        'decrease_brightness': 'AdjustDownBrightness',
        'set_brightness': 'SetBrightness',
        'increase_temperature': 'AdjustUpTemperature',
        'decrease_temperature': 'AdjustDownTemperature',
        'set_temperature': 'SetTemperature',
        'set_color': 'SetColor',
        'pause': 'Pause',
        'continue': 'Continue',
        'play': 'Play',
        'query_color': 'QueryColor',
        'query_power_state': 'QueryPowerState',
        'query_temperature': 'QueryTemperature',
        'query_humidity': 'QueryHumidity',
        'set_mode': 'SetMode'
        # '': 'QueryWindSpeed',
        # '': 'QueryBrightness',
        # '': 'QueryFog',
        # '': 'QueryMode',
        # '': 'QueryPM25',
        # '': 'QueryDirection',
        # '': 'QueryAngle'
    }
    _device_type_alias = {
        'television': '电视',
        'light': '灯',
        'aircondition': '空调',
        'airpurifier': '空气净化器',
        'outlet': '插座',
        'switch': '开关',
        'roboticvacuum': '扫地机器人',
        'curtain': '窗帘',
        'humidifier': '加湿器',
        'fan': '风扇',
        'bottlewarmer': '暖奶器',
        'soymilkmaker': '豆浆机',
        'kettle': '电热水壶',
        'waterdispenser': '饮水机',
        'camera': '摄像头',
        'router': '路由器',
        'cooker': '电饭煲',
        'waterheater': '热水器',
        'oven': '烤箱',
        'waterpurifier': '净水器',
        'fridge': '冰箱',
        'STB': '机顶盒',
        'sensor': '传感器',
        'washmachine': '洗衣机',
        'smartbed': '智能床',
        'aromamachine': '香薰机',
        'window': '窗',
        'kitchenventilator': '抽油烟机',
        'fingerprintlock': '指纹锁',
        'telecontroller': '万能遥控器',
        'dishwasher': '洗碗机',
        'dehumidifier': '除湿机',
        'dryer': '干衣机',
        'wall-hung-boiler': '壁挂炉',
        'microwaveoven': '微波炉',
        'heater': '取暖器',
        'mosquitoDispeller': '驱蚊器',
        'treadmill': '跑步机',
        'smart-gating': '智能门控',
        'smart-band': '智能手环',
        'hanger': '晾衣架',
        'bloodPressureMeter': '血压仪',
        'bloodGlucoseMeter': '血糖仪',
    }

    device_type_map_h2p = {
        'climate': 'aircondition',
        'fan': 'fan',
        'light': 'light',
        'media_player': 'television',
        'remote': 'telecontroller',
        'switch': 'switch',
        'sensor': 'sensor',
        'cover': 'curtain',
        'vacuum': 'roboticvacuum',
        }

    _service_map_p2h = {
        # 测试，暂无找到播放指定音乐话术，继续播放指令都是Play
        # 'media_player': {
        #     'Play': lambda state, attributes, payload: (['play_media'], ['play_media'], [{"media_content_id": payload['value'], "media_content_type": "playlist"}]),
        #     'Pause': 'media_pause',
        #     'Continue': 'media_play'
        # },
        # 模式和平台设备类型有关，自动模式 静音模式 睡眠风模式（fan类型） 睡眠模式（airpurifier类型）
        'fan': {
            'setpowerstate':        lambda state, attributes, payload: (['fan'], ['turn_on' if payload['value'] else 'turn_off'],[{}]),
            
            # 'SetMode': lambda state, attributes, payload: (['fan'], ['set_speed'], [{"speed": payload['value']}])
        },
        'cover': {
            'TurnOn':  'open_cover',
            'TurnOff': 'close_cover',
            'Pause': 'stop_cover',
        },
        'vacuum': {
            'TurnOn':  'start',
            'TurnOff': 'return_to_base',
        },
        'light': {
            'setpowerstate':        lambda state, attributes, payload: (['light'], ['turn_on' if payload['value'] else 'turn_off'],[{}]),
            'setcolor':             lambda state, attributes, payload: (['light'], ['turn_on'], [{"color_name": payload['value']}]),
            'setbrightness':        lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': payload['value']}]),
            'adjustbrightness':     lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': max(min(attributes['brightness_pct'] + payload['value'], 100),0)}]),
            # 'setcolorTemperature':  lambda state, attributes, payload: (['light'], ['turn_on'], [{'color_temp': payload['value']}]), 
            # 'adjustcolorTemperature': lambda state, attributes, payload: (['light'], ['turn_on'], [{'color_temp': max(min(attributes['color_temp'] + payload['value'], 100),0)}]),

            # 'TurnOn':  'turn_on',
            # 'TurnOff': 'turn_off',
            # 'SetBrightness':        lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': payload['value']}]),
            # 'AdjustUpBrightness':   lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': min(attributes['brightness_pct'] + payload['value'], 100)}]),
            # 'AdjustDownBrightness': lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': max(attributes['brightness_pct'] - payload['value'], 0)}]),
            # 'SetColor':             lambda state, attributes, payload: (['light'], ['turn_on'], [{"color_name": payload['value']}])
        },
        'havcs':{
            'TurnOn': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_on']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_on']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_on']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),
            'TurnOff': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_off']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_off']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_off']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_off'], [{}]),
            'AdjustUpBrightness': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increase_brightness']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increase_brightness']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increase_brightness']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),
            'AdjustDownBrightness': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_brightness']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_brightness']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_brightness']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),
        }

    }
    # action:[{Platfrom Attr: HA Attr},{}]
    _query_map_p2h = {

    }

class VoiceControlAligenie(PlatformParameter, VoiceControlProcessor):
    def __init__(self, hass, mode, entry, zone_constraints, device_name_constraints):
        self._hass = hass
        self._mode = mode
        self._zone_constraints = zone_constraints
        self._device_name_constraints = device_name_constraints
        # try:
        #     self._zone_constraints  = json.loads(urlopen('https://open.bot.tmall.com/oauth/api/placelist').read().decode('utf-8'))['data']
        #     self._device_name_constraints = json.loads(urlopen('https://open.bot.tmall.com/oauth/api/aliaslist').read().decode('utf-8'))['data']
        #     self._device_name_constraints.append({'key': '电视', 'value': ['电视机']})
        #     self._device_name_constraints.append({'key': '传感器', 'value': ['传感器']})
        # except:
        #     self._zone_constraints = []
        #     self._device_name_constraints = []
        #     import traceback
        #     _LOGGER.info("[%s] can get places and aliases data from website, set None.\n%s", LOGGER_NAME, traceback.format_exc())
        self.vcdm = VoiceControlDeviceManager(entry, DOMAIN, self.device_action_map_h2p, self.device_attribute_map_h2p, self._service_map_p2h, self.device_type_map_h2p, self._device_type_alias, self._device_name_constraints, self._zone_constraints)

    def _errorResult(self, errorCode, messsage=None):
        """Generate error result"""
        messages = {
            'INVALIDATE_CONTROL_ORDER': 'invalidate control order',
            'SERVICE_ERROR': 'service error',
            'DEVICE_NOT_SUPPORT_FUNCTION': 'device not support',
            'INVALIDATE_PARAMS': 'invalidate params',
            'DEVICE_IS_NOT_EXIST': 'device is not exist',
            'IOT_DEVICE_OFFLINE': 'device is offline',
            'ACCESS_TOKEN_INVALIDATE': ' access_token is invalidate'
        }
        return {'errorCode': errorCode, 'message': messsage if messsage else messages[errorCode]}

    async def handleRequest(self, data, auth = False, request_from = "http"):
        """Handle request"""
        _LOGGER.info("[%s] Handle Request:\n%s", LOGGER_NAME, data)

        header = self._prase_command(data, 'header')
        payload = self._prase_command(data, 'payload')
        action = self._prase_command(data, 'action')
        namespace = self._prase_command(data, 'namespace')
        properties = None
        content = {}
        self._currentDevice = 0
        err_result = 0
        if auth:
            if namespace == 'AliGenie.Iot.Device.Discovery':
                err_result, discovery_devices, entity_ids = self.process_discovery_command(request_from)
                content = {'devices': discovery_devices}
            elif namespace == 'AliGenie.Iot.Device.Control' or namespace == 'AliGenie.Iot.Device.Query':
                deviceIds = self._prase_command(data, 'device_ids')
                content['deviceResponseList'] = []
                for deviceId in deviceIds:
                    if namespace == 'AliGenie.Iot.Device.Control':
                        err_result, res = await self.process_control_command(data)

                    elif namespace == 'AliGenie.Iot.Device.Query':
                        err_result, res = self.process_query_command(data)

                    device_json = {}
                    device_json['deviceId'] = deviceId
                    if err_result:
                        device_json['errorCode'] = err_result
                        device_json['message'] = "Failed to control device: %s" % deviceId
                    else:
                        device_json['errorCode'] = "SUCCESS"
                        device_json['message'] = "SUCCESS"
                    content['deviceResponseList'].append(device_json)
                    self._currentDevice = self._currentDevice + 1
                err_result = 0
            else:
                err_result = self._errorResult('SERVICE_ERROR')
        else:
            err_result = self._errorResult('ACCESS_TOKEN_INVALIDATE')

        # Check error and fill response name
        if err_result:
            header['name'] = 'ErrorResponse'
            content = err_result
        else:
            header['name'] = 'CorrectResponse'

        # Fill response deviceId

        response = {'header': header, 'payload': content}
        _LOGGER.info("[%s] Respnose:\n%s", LOGGER_NAME, response)
        return response

    def _prase_command(self, command, arg):
        header = command['header']
        payload = command['payload']
        if arg == "device_ids":
            return payload['deviceIds']
        elif arg == 'device_id':
            return payload['deviceIds'][self._currentDevice]
        elif arg == 'action':
            if header['name'] == "DiscoveryDevices":
                return header['name']
            elif header['name'] == "thing.attribute.set":
                act = "set"
            elif header['name'] == "thing.attribute.adjust":
                act = "adjust"
            else:
                _LOGGER.error("[%s] Unkonw action: %s", LOGGER_NAME, header['name'])
            _LOGGER.info(payload['params']);
            for key,value in payload['params'].items():
                act = act + key
                payload['value'] = value
            return act
        elif arg == 'user_uid':
            return payload.get('openUid','')
        elif arg == 'namespace':
            return header['namespace']
        else:
            return command.get(arg)

    def _discovery_process_propertites(self, device_properties):
        properties = []
        for device_property in device_properties:
            name = self.device_attribute_map_h2p.get(device_property.get('attribute'))
            state = self._hass.states.get(device_property.get('entity_id'))
            if name:
                value = state.state if state else 'unavailable'
                properties += [{'name': name.lower(), 'value': value}]
        return properties if properties else [{'name': 'powerstate', 'value': 'off'}]
    
    def _discovery_process_actions(self, device_properties, raw_actions):
        actions = []
        for device_property in device_properties:
            name = self.device_attribute_map_h2p.get(device_property.get('attribute'))
            if name:
                action = self.device_action_map_h2p.get('query_'+name)
                if action:
                    actions += [action,]
        for raw_action in raw_actions:
            action = self.device_action_map_h2p.get(raw_action)
            if action:
                actions += [action,]
        return list(set(actions))

    def _discovery_process_device_type(self, raw_device_type):
        # raw_device_type guess from device_id's domain transfer to platform style
        return raw_device_type if raw_device_type in self._device_type_alias else self.device_type_map_h2p.get(raw_device_type)

    def _discovery_process_device_info(self, device_id,  device_type, device_name, zone, properties, actions):
        if device_type == "light":
            model = "Light1"
        elif device_type == "fan":
            model = "Fan1"
        return {
            'deviceId': encrypt_device_id(device_id),
            'deviceName': device_name,
            'deviceType': device_type,
            'zone': zone,
            'model': model,
            'brand': 'IOTZONE',
            'icon': 'https://d33wubrfki0l68.cloudfront.net/cbf939aa9147fbe89f0a8db2707b5ffea6c192cf/c7c55/images/favicon-192x192-full.png',
            'properties': properties,
            'actions': actions
            #'extensions':{'extension1':'','extension2':''}
        }


    def _control_process_propertites(self, device_properties, action) -> None:
        return {}

    def _query_process_propertites(self, device_properties, action) -> None:
        properties = []
        action = action.replace('Request', '').replace('Get', '')
        if action in self._query_map_p2h:
            for property_name, attr_template in self._query_map_p2h[action].items():
                formattd_property = self.vcdm.format_property(self._hass, device_properties, attr_template)
                properties.append({property_name:formattd_property})
        else:
            for device_property in device_properties:
                state = self._hass.states.get(device_property.get('entity_id'))
                value = state.attributes.get(device_property.get('attribute'), state.state) if state else None
                if value:
                    if action == 'Query':
                        formattd_property = {'name': self.device_attribute_map_h2p.get(device_property.get('attribute')), 'value': value}
                        properties.append(formattd_property)
                    elif device_property.get('attribute') in action.lower():
                        formattd_property = {'name': self.device_attribute_map_h2p.get(device_property.get('attribute')), 'value': value}
                        properties = [formattd_property]
                        break
        return properties

    def _decrypt_device_id(self, device_id) -> None:
        return decrypt_device_id(device_id)