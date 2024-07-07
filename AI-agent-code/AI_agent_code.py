from dashscope.api_entities.dashscope_response import Message

from person import Judger
from coder import ProductManager
from writer import Writer, Novel, FeedbackCommenters

def main():
    novel = Novel()
    novel.type = "爱情"
    novel.target_readers = "女性"
    novel.basic_settings = "现实世界，现代，中国"
    novel.topic = "女性成长"
    novel.conflicts = "老公不管家，不尊重老婆的劳动成果"
    novel.roles = "老公的特点：大男子主义，比较自私，老婆的特点：很传统。目标：女性觉醒"

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

