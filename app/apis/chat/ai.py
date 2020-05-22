import os
import json

def process_messages(config_dir, app, content):
    need_to_reply = False

    # find reply template
    cfg_file = os.path.join(config_dir, 'reply_template.json')
    with open(cfg_file, 'r', encoding='utf-8') as f:
        cfg_json = json.load(f)

    
    for key, values in cfg_json.items():
        if key.strip().upper() == content.strip().upper():
            need_to_reply = True
            response = ""
            for v in values:
                response = response + v + "\n"

            response.rstrip()
    
    # find posts
    if not need_to_reply:

        response = ""

        articles = app.articles

        if articles is not None:

            for key, values in articles.items():
                if content.strip().upper() in key.strip().upper():
                    need_to_reply = True
                    response = response + key + '(' + values[0] + ')' + "\n"

            response.rstrip()

    # fallback
    if not need_to_reply:
        need_to_reply = True
        response = "感谢您参与留言，信息已收到，我会定期回复!"
        response = response + '\n\n' + \
                   '=====\n' + \
                   '本公众号后端由Python提供搜索支持，您也可以尝试发送关键字，搜索本站提供的文章，英文不区分大小写，例如：\n' + \
                   '\n' + \
                   '发送 "PyQt" 获取PyQt相关文章\n' + \
                   '发送 "pandas" 获取pandas相关文章\n' + \
                   '发送 "资源列表" 获取代码资源\n' + \
                   '等等'
        

    return need_to_reply, response