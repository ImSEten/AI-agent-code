from dashscope.api_entities.dashscope_response import Message

from person import Judger
from writer import Writer, Novel

def main():
    novel = {}
    novel["类型"] = "爱情"
    novel["目标读者"] = "女性"
    novel["基本设定"] = "现实世界，现代，中国"
    novel["主题"] = "女性成长"
    novel["主要冲突"] = "老公不管家，不尊重老婆的劳动成果"
    novel["角色特点"] = "老公的特点：大男子主义，比较自私\n老婆的特点：很传统。\n目标：女性觉醒"
    novel["字数"] = "10万字"

    message = Message(role="user", content="我想写一篇小说。")
    judger = Judger()
    thought = judger.ask_models(message)
    # print("thought =", thought)
    # print("message = ", message)

    if thought == judger.Thought.thought_require:
        print("thout is require")
        writer = Writer(novel=novel)
        answer = writer.ask_models(message)
        print("answer =", answer)
        pass # if thought == thought_require
    #product_manager = ProductManager()
    #product_manager.ask_models(message)
    pass # function main


main()















# while True:
#     message = input('user:')
#     default_messages.append({'role': Role.USER, 'content': message})
#     whole_message = ''
#     responses = Generation.call(Generation.Models.qwen_turbo, 
#                                 messages=default_messages, 
#                                 result_format='message', 
#                                 stream=True, 
#                                 incremental_output=True)
#     print('system:',end='')
#     for response in responses:
#         whole_message += response.output.choices[0]['message']['content']
#         print(response.output.choices[0]['message']['content'], end='')
#     print()
#     default_messages.append({'role': 'assistant', 'content': whole_message})

