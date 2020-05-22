# -*- coding: utf-8 -*-
import hashlib

from flask import Flask, Blueprint, current_app, request, make_response
from flask_restx  import Namespace, Resource, fields

from app.apis.chat import receive, reply
from app.apis.chat.ai import process_messages


ns = Namespace('chat', description='provide chat functionalities')


@ns.route('/message', strict_slashes=False)
class MessageResourceHandler(Resource):
    def post(self):
        try:
            webData = request.get_data(as_text=True)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName

                current_app.logger.info("received {} from: {}".format(recMsg.Content, fromUser))


                need_to_reply, content = process_messages(current_app.config.get('CONFIG_DIR'), 
                                                          current_app,
                                                          recMsg.Content)

                replyMsg = reply.TextMsg(toUser, fromUser, content)
                send = replyMsg.send()
                current_app.logger.info(send)
                if need_to_reply:
                    return make_response(send)
                else:
                    return "success"
            elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'event':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.EventType == 'subscribe':
                    current_app.logger.info("subscribe event is received from {}".format(toUser))
                    content = '来Python酷学Python库，欢迎您关注本公众号，我们致力于提供Python库相关的原创技术性文章，' + \
                              '可以访问我们的主页\nhttps://pythonlibrary.net\n' + \
                              '\n' + \
                              '本公众号后端由Python提供搜索支持，您可以尝试发送关键字，搜索本站提供的文章，英文不区分大小写，例如：\n' + \
                              '\n' + \
                              '发送 "PyQt" 获取PyQt相关文章\n' + \
                              '发送 "pandas" 获取pandas相关文章\n' + \
                              '发送 "资源列表" 获取代码资源\n' + \
                              '等等'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    send = replyMsg.send()
                    current_app.logger.info(send)
                    return make_response(send)
                else:
                    return "success"
            else:
                current_app.logger.info("received message is not supported")
                return "success"
        except Exception as e:
            current_app.logger.error(e)
            return "success"

    def get(self):
        try:
            signature = request.args.get('signature')
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            echostr = request.args.get('echostr')
            token = current_app.config.get('WEIWIN_TOKEN')

            info_list = [token.encode(), timestamp.encode(), nonce.encode()]
            info_list.sort()
            sha1 = hashlib.sha1()
            for info in info_list:
                sha1.update(info)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                current_app.logger.info("hash and signature match")
                return int(echostr)
            else:
                current_app.logger.info("hash and signature dont match")
                return ""
        except Exception as e:
            current_app.logger.info(e)
            return ""
