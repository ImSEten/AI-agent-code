from dashscope.api_entities.dashscope_response import Message
from person import Person

class Novel():
    def __init__(self):
        # **类型**：你想写的是哪种类型的小说？比如科幻、悬疑、爱情、奇幻、冒险、犯罪、成长、历史或其他？
        self.type = ""
        # **目标读者群**：你的目标读者是谁？这会影响故事的语言风格和复杂程度。
        self.target_readers = ""
        # **基本设定**：故事发生在哪里？是现实世界的一个特定时期，还是一个虚构的世界？
        self.basic_settings = ""
        # **主题或核心思想**：你希望传达给读者的主要信息或情感是什么？
        self.topic = ""
        # **主要冲突**：故事的核心冲突是什么？这可以是一个人物的内心挣扎，也可以是外部的挑战。
        self.conflicts = ""
        # **主要角色**：主角的性格特点，他们的目标、动机和转变点是什么？
        self.roles = ""
        # **字数**: 文章大概字数
        self.numbers = "10万字"
        # **章节数**: 文章大概章节数(一章约1000字)
        self.chapters = "100章"
        # **约束**: 文章的一些约束，比如不要出现英文，名字必须是中文，不能有英文名字等
        self.restraint = "不能出现英文，名字必须是中文。不要有总结性的言论。\n"
        # **第一视角**: 文章的第一视角是谁，即“我”是谁
        self.me = "女主"

        # **故事构思**: 由构思顾问生成
        self.ideation = ""
        # **故事大纲**: 由大纲规划生成
        self.outline = ""
        pass # function __init__
    pass # class Novel

class Writer(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = ""
        self.message = ""
        self.ideation_consultant = IdeationConsultant(novel=novel)
        self.outline_planner = OutlinePlanner(novel=novel)
        self.role_planner = RolePlanner(novel=novel)
        pass # function __init__

    def check_history(self):
        if not self.history: # this is mean I don't ask the model onece, so initial the first questions.

            pass # if not self.history
        pass # function check_history

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        # start generate roleplanner's prompt

        # end generate Writer's prompt
        message.content += self.message
        return message
        pass # function generate_prompt

    def ask_models(self, new_message: Message) -> Message:
        # 构思顾问：搭建故事框架
        message = self.ideation_consultant.generate_prompt(new_message=new_message)
        ideation = self.ideation_consultant.ask_models(new_message=message)
        print("IdeationConsultant answer =", ideation)
        self.novel.ideation = ideation.content
        # 大纲规划：搭建故事大纲
        message = self.outline_planner.generate_prompt(new_message=new_message)
        outline = self.outline_planner.ask_models(new_message=message)
        print("OutlinePlanner answer =", outline)
        self.novel.outline = outline.content
        # 角色规划：搭建角色性格
        message = self.role_planner.generate_prompt(new_message=new_message)
        roles = self.role_planner.ask_models(new_message=message)
        self.novel.roles = roles.content
        print("RolePlanner answer =", roles)

        # 写作
        for i in range(10):
            worker = Worker(self.novel, id=i)
            message = worker.generate_prompt(new_message=new_message)
            answer = worker.ask_models(new_message=message)
            print("worker org answer =", answer)
            # 反馈
            feedback = FeedbackCommenters(self.novel)
            message = feedback.generate_prompt(new_message=answer)
            answer = feedback.ask_models(new_message=message)
            # print("FeedbackCommenters answer =", answer)

            message = Message(role=message.role, content=answer.content)
            answer = worker.ask_models(new_message=message)
            print("worker edited answer =", answer)
            pass # for i
        
        
        #message = self.generate_prompt(new_message=new_message)
        #return super().ask_models(message)
        pass #function ask_models
    pass # class ProductManager

# IdeationConsultant: 构思顾问：头脑风暴，讨论故事的主题、情节、主要角色和背景设定，帮你构建初步的故事框架。
class IdeationConsultant(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = "构思顾问"
        self.message = "\n你是一个" + self.role + '，构建故事的主题、情节、主要角色和背景设定，构建初步的故事框架。'
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        novel_description = "小说的一些约束：" + self.novel.restraint + "小说的类型是" + self.novel.type + "，目标读者是" + self.novel.target_readers + "，基本设定是" + self.novel.basic_settings + "，主题是" + self.novel.topic + "，主要冲突是" + self.novel.conflicts + "，主要角色是" + self.novel.roles
        novel_description += "\n文章约" + self.novel.numbers + "，约" + self.novel.chapters
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        message.content += novel_description
        message.content += self.message
        return message
        pass # function generate_prompt
    pass # class IdeationConsultant

# OutlinePlanner: 大纲规划：我们可以一起讨论并制定故事的大纲，确保故事结构清晰，逻辑连贯。
class OutlinePlanner(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = "大纲规划"
        self.message = "\n你是一个" + self.role + "，制定故事的大纲，确保故事结构清晰，逻辑连贯。"
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        message.content += self.novel.ideation
        message.content += "文章约" + self.novel.numbers + "，约" + self.novel.chapters
        message.content += self.message
        return message
        pass # function generate_prompt
    pass # class OutlinePlanner

# RolePlanner: 角色规划：我可以协助您深入挖掘和塑造人物的性格特征，让角色更有生命力。
class RolePlanner(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = "角色规划"
        self.message = "\n你是一个" + self.role + "，深入挖掘和塑造人物的性格特征，让角色更有生命力。"
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        # start generate roleplanner's prompt
        message.content += self.novel.ideation
        message.content += self.novel.outline
        message.content += self.message
        return message
        pass # function generate_prompt
    pass # class RolePlanner

# WriteGuidance: 写作指导：对于故事中的关键转折点或冲突，我会提供反馈和建议，以保持故事的紧张感和吸引力。
class WriteGuidance(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = "写作指导"
        self.message = "\n你是一个" + self.role + "，对于故事中的关键转折点或冲突，请你提供反馈和建议，以保持故事的紧张感和吸引力。"
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        message.content += self.message
        return message
        pass # function generate_prompt
    pass # class WriteGuidance

# LanguageGuidance: 语言指导：我可以提供关于句子结构、词汇选择、风格指导等写作技巧，帮助提升您的文笔。
class LanguageGuidance(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = "语言指导"
        self.message = "\n你是一个" + self.role + "，请提供关于句子结构、词汇选择、风格指导等写作技巧，帮助提升您的文笔。"
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        message.content += self.message
        return message
        pass # function generate_prompt
    pass # class LanguageGuidance

# FeedbackCommenters: 反馈评论：当你有部分章节或草稿时，我可以阅读并给出修改意见，帮助你打磨文笔和剧情连贯性。
class FeedbackCommenters(Person):
    def __init__(self, novel: Novel):
        super().__init__()
        self.novel = novel
        self.role = "反馈评论者"
        self.message = "\n你是一个" + self.role + "，请阅读以下内容并给出修改意见，帮助打磨文笔和剧情连贯性"
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role="user", content=new_message.content)
        message = super().generate_prompt(new_message=message)
        message.content = self.message + message.content
        return message
        pass # function generate_prompt
    pass # class FeedbackCommenters

# Worker: 苦比打工人。
class Worker(Person):
    def __init__(self, novel: Novel, id: int):
        super().__init__()
        # id: 打工人编号
        self.id = id
        self.novel = novel
        self.role = "作家"
        self.message = "\n你是一个" + self.role + "，请按照提供的信息写第" + str(id) + "章，约1000个汉字，不要有总结，文章采用第一视角，“我”是" + self.novel.me
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        # start generate worker's prompt
        message.content += self.novel.restraint
        message.content += "文章约" + self.novel.numbers + "，约" + self.novel.chapters
        message.content += self.novel.ideation
        message.content += self.novel.outline
        message.content += self.novel.roles
        message.content += self.message
        return message
        pass # function generate_prompt
    pass # class Worker