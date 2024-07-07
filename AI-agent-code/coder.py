from dashscope.api_entities.dashscope_response import Message
from person import Person

class ProductManager(Person):
    message_before = "我这里有一个需求：\n"
    def check_history(self):
        if not self.history: # this is mean I don't ask the model onece, so initial the first questions.

            pass # if not self.history
        pass # function check_history

    def generate_prompt(self, new_message: Message) -> Message:
        new_message.content = self.message_before + new_message.content
        message = super().generate_prompt(new_message=new_message)
        message.content += "请拆分这个需求。"
        return message
        pass # function generate_prompt

    def ask_models(self, new_message: Message) -> Message:
        message = self.generate_prompt(new_message=new_message)
        return super().ask_models(message)
        pass #function ask_models
    pass # class ProductManager