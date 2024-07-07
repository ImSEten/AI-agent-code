from typing import List
from http import HTTPStatus

from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from dashscope.api_entities.dashscope_response import Message
import dashscope

dashscope.api_key="sk-62996713ee5a4b67a0d51ab207a1f2df"

default_messages=[{"role":"system","content":"You are a helpful assistant."}]

# call_api send the question to the remote mdels on internet
def call_api(messages: List[Message]) -> Message:
    whole_message: str = ""
    role: str = ""
    responses = Generation.call(Generation.Models.qwen_turbo, 
                                messages=messages, 
                                result_format="message", 
                                stream=True, 
                                incremental_output=True)
    #print("AI:", end='')
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            whole_message += response.output.choices[0]["message"]["content"]
            if not role:
                role = response.output.choices[0]["message"]["role"]
                #print("role:", role, end='\t')
                pass # if not role
            #print(response.output.choices[0]["message"]["content"], end='')
            pass # if
        else:
            print("Request id: %s, Status code: %s, error code: %s, error message: %s" % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return None
            pass # else
        pass # for response in responses
    #print()
    return Message(role=role, content=whole_message)
    pass # function call_api