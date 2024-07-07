from typing import List
from dashscope.api_entities.dashscope_response import Message
from common import call_api
import enum

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

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        if message.content[-1] == "\n":
            pass
        elif message.content[-1] == "." or message.content[-1] == "。" or message.content[-1] == "，" or message.content[-1] == "," or message.content[-1] == "!" or message.content[-1] == "！" or message.content[-1] == "?" or message.content[-1] == "？":
            message.content += "\n"
            pass # if new_message.content[-1]
        else:
            message.content += "。\n"
        return message
        pass # function generate_prompt

    # generate_prompt will generate prompt from history
    def generate_prompt_from_history(self, new_message: Message) -> List[Message]:
        messages = self.history
        messages.append(new_message)
        return messages
        pass # function generate_prompt_from_history

    # ask_models send the question to the AI models
    def ask_models(self, new_message: Message) -> Message:
        # print("ask_models new_message = ", new_message)
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
        thoght_unkown = enum.auto()
        pass # class Thought

    def generate_prompt(self, new_message: Message) -> Message:
        message = super().generate_prompt(new_message=new_message)
        message.content += "请分析我的想法是一个需求还是仅聊天，请回答是需求或聊天，不要解释。"
        return message
        pass # function generate_prompt

    def judge_requere_or_chat(self, answer: Message) -> Thought:
        if answer.content == "需求" or answer.content == "需求。":
            return self.Thought.thought_require
        elif answer.content == "聊天" or answer.content == "聊天。":
            return self.Thought.thought_require
        else:
            return self.Thought.thoght_unkown
        pass # function judge_require_or_chat will check the thought, and distribute tasks to product managers or chatbots.

    def ask_models(self, new_message: Message) -> Thought:
        message = self.generate_prompt(new_message=new_message)
        # print("judger message = ", message)
        # print("judger new_message = ", new_message)
        answer = super().ask_models(new_message=message)
        # print("judger message after ask_models = ", message)
        # print("judger new_message after ask_models = ", new_message)
        thought = self.judge_requere_or_chat(answer=answer)
        return thought
        pass # function ask, ask for module, and judge if the message is a requirement or chat.
    pass # class Judger