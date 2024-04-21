from typing import List, Dict
from http import HTTPStatus
import enum

from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from dashscope.api_entities.dashscope_response import Message
import dashscope

dashscope.api_key="sk-62996713ee5a4b67a0d51ab207a1f2df"

default_messages=[{"role":"system","content":"You are a helpful assistant."}]

# class Message:
#     def __init__(self, role: str, content: str):
#         self.data = {
#             "role": role, 
#             "content": content
#             }
#         pass # function __init__
#     pass # class Message

# call_api send the question to the remote mdels on internet
def call_api(messages: List[Message]) -> Message:
    whole_message: str = ""
    role: str = ""
    responses = Generation.call(Generation.Models.qwen_turbo, 
                                messages=messages, 
                                result_format="message", 
                                stream=True, 
                                incremental_output=True)
    print("AI:", end='')
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            whole_message += response.output.choices[0]["message"]["content"]
            if not role:
                role = response.output.choices[0]["message"]["role"]
                print("role:", role, end='\t')
                pass # if not role
            print(response.output.choices[0]["message"]["content"], end='')
            pass # if
        else:
            print("Request id: %s, Status code: %s, error code: %s, error message: %s" % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return None
            pass # else
        pass # for response in responses
    print()
    return Message(role=role, content=whole_message)
    pass # function call_api

class Person(object):
    def __init__(self):
        self.history: List[Message] = []
        pass # function __init__

    # record_history will record the chat history to self.history
    # this function should only be call after successfully call the api.
    def record_history(self, interlocution: List[Message]):
        for i in interlocution:
            self.history.append(i)
            pass # for i in interlocution
        pass # function record_history

    # generate_prompt will generate prompt from history
    def generate_prompt_from_history(self, new_message: Message) -> List[Message]:
        messages = self.history
        messages.append(new_message)
        return messages
        pass # function generate_prompt_from_history

    # ask_models send the question to the AI models
    def ask_models(self, new_message: Message) -> Message:
        messages = self.generate_prompt_from_history(new_message)
        messages.append(new_message)
        answer = call_api(messages)
        self.record_history([new_message, answer])
        return answer
        pass # function ask_models
    pass # class Person

# class Judger mean he will judge the input whether a require or a chat
class Judger(Person):
    # Thought is the enum, which has require, chat
    class Thought(enum.Enum):
        thought_require = enum.auto()
        thought_chat = enum.auto()
        pass # class Thought

    def generate_prompt(self, new_message: Message) -> Message:
        if new_message.content[-1] == "." or new_message.content[-1] == "。" or new_message.content[-1] == "，" or new_message.content[-1] == "," or new_message.content[-1] == "!" or new_message[-1] == "！" or new_message[-1] == "?" or new_message[-1] == "？":
            new_message.content += "。"
            pass # if new_message.content[-1]
        new_message.content += "请分析我的想法是一个需求还是仅聊天，请回答是需求或聊天，不要解释。"
        return new_message
        pass # function generate_prompt

    def judge_requere_or_chat(self, answer: Message) -> Thought:
        if answer.content == "需求":
            return self.Thought.thought_require
        pass # function judge_require_or_chat will check the thought, and distribute tasks to product managers or chatbots.
    pass # class Judger

class ProductManager(Person):
    def check_history(self):
        if not self.history: # this is mean I don't ask the model onece, so initial the first questions.

            pass # if not self.history

        pass # function check_history
    pass # class ProductManager

def main():
    message = Message(role="user", content="我想要一个自动贩卖机的软件代码实现。")
    product_manager = ProductManager()
    product_manager.ask_models(message)
    pass


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

