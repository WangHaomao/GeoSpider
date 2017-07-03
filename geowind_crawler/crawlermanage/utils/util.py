# -*- encoding: utf-8 -*-
from crawlermanage.utils.message import Message
from crawlermanage.utils.settings_helper import get_attr


def is_open():
    messager = Message(get_attr('LOCAL_HOST'))
    messager.subscribe('crawler')
    msg = 'is_start'
    messager.publish('crawler', msg)
    receive = messager.listen()
    print(receive)
    if receive == 'master:is_start':
        return True
    return False


if __name__ == '__main__':
    print(is_open())