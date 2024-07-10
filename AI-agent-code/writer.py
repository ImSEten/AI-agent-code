from dashscope.api_entities.dashscope_response import Message
from person import Person
import re

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

        # **故事大纲**: 由大纲规划生成
        self.outline = ""
        pass # function __init__
    pass # class Novel

class Writer(Person):
    def __init__(self, novel: dict):
        super().__init__()
        self.novel = novel
        self.role = ""
        self.message = ""
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
        # 大纲规划：搭建故事大纲
        message = self.outline_planner.generate_prompt(new_message=new_message)
        outline = self.outline_planner.ask_models(new_message=message)
        self.novel["大纲"] = self.outline_planner.extract_content_regex(outline.content)
        print("OutlinePlanner answer =\n", outline.content)
        print("OutlinePlanner answer org =", outline)

        # 角色规划：搭建角色性格
        message = self.role_planner.generate_prompt(new_message=new_message)
        roles = self.role_planner.ask_models(new_message=message)
        self.novel["角色档案"] = self.role_planner.extract_content_regex(roles.content)
        print("RolePlanner answer =", roles.content)
        print("RolePlanner answer org =", roles.content)
        print("self.novel =\n", self.novel)
        worker = Worker(self.novel, id=1)
        for i in range(2):
            message = worker.generate_prompt(new_message=new_message)
            content = worker.ask_models(message)
            print("content =\n", content.content)
        # # 写作
        # for i in range(10):
        #     worker = Worker(self.novel, id=i)
        #     message = worker.generate_prompt(new_message=new_message)
        #     answer = worker.ask_models(new_message=message)
        #     print("worker org answer =", answer)
        #     # 反馈
        #     feedback = FeedbackCommenters(self.novel)
        #     message = feedback.generate_prompt(new_message=answer)
        #     answer = feedback.ask_models(new_message=message)
        #     # print("FeedbackCommenters answer =", answer)

        #     message = Message(role=message.role, content=answer.content)
        #     answer = worker.ask_models(new_message=message)
        #     print("worker edited answer =", answer)
        #     pass # for i
        
        
        #message = self.generate_prompt(new_message=new_message)
        #return super().ask_models(message)
        pass #function ask_models
    pass # class ProductManager

# OutlinePlanner: 大纲规划：制定故事的大纲，确保故事结构清晰，逻辑连贯。
class OutlinePlanner(Person):
    def __init__(self, novel: dict):
        super().__init__()
        self.novel = novel
        self.prompt = """
# Role:
网络小说作家，以剧情不落入俗套闻名
## Background And Goals:
你正在构思一部长篇网络小说，但是你还没有一个完整的大纲，你希望有一个合理的剧情和设定，为写作做好准备。你能够使这部小说新颖，有情感共鸣，有爽点，吸引读者。
你应该根据用户输入的想法和要求，思考合理的剧情和设定，输出小说的大纲。
## Inputs:
想法、要求，请按此构思大纲
## Outputs:
以固定格式输出，不要有其他格式外的输出：
```
# 大纲
设定、主要人物、开端发展高潮结局等
# END
```
## Workflows:
你会按下面的框架来实现目标
- 理解用户输入的想法要求
- 特别重要！避开套路，做到新颖
    + 想象一个语不惊人死不休的展开，吸引读者的注意
    + 特别重要！可以是轻松的喜剧，也可以是悲剧，或者是平淡的故事，但一定要有情感共鸣
- 尝试在故事的发展中制造爽点，让读者兴奋不已
- 构造一个出人意料的反转，但又在情理之中，让读者感到惊喜
- 将故事发展到一个令人瞠目结舌的高潮，让读者感受到剧情的魅力
- 最后将故事情节巧妙地颠覆，给读者带来意想不到的结局
- 探讨故事的意义，思考故事的深层内涵
- 回顾整个大纲，思考合理的剧情和设定，作出调整
- 输出小说的大纲
## init:
接下来，我会提供给你小说的要求，我希望你可以完全的理解之后再写大纲。
"""
        init = self.ask_models(new_message=Message(role="user", content=self.prompt))
        print("OutlinePlanner init =", init.content)
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        # message.content += self.novel.ideation
        # message.content += "文章约" + self.novel.numbers + "，约" + self.novel.chapters
        # message.content += self.message
        for k, v in self.novel.items():
            message.content += f"# {k}\n{v}\n\n"
        return message
        pass # function generate_prompt

    def extract_content_regex(self, text: str) -> str:
        # 匹配以# 大纲开始，直到# END或**END**为止的内容
        #pattern = r'(?:# 大纲\n|\n# 大纲\n)(.*?)(?:# END|\*\*END\*\*|# END\n|\*\*END\*\*\n)'
        pattern = r'(?:# 大纲)(.*?)(?:# END*?|\*\*END*?)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            s = text.strip().split("# 大纲\n")
            if len(s) < 1:
                return text
            else:
                return s[1]
            pass # end if
        pass # function extract_content_regex
    pass # class OutlinePlanner

# RolePlanner: 角色规划：我可以协助您深入挖掘和塑造人物的性格特征，让角色更有生命力。
class RolePlanner(Person):
    def __init__(self, novel: dict):
        super().__init__()
        self.novel = novel
        self.role = "角色规划"
        self.message = "\n你是一个" + self.role + "，深入挖掘和塑造人物的性格特征，让角色更有生命力。"
        self.prompt = """
# Role:
网络小说作家，专注于塑造鲜活且多维的人物角色

## Background and Goals:
你正在为一部引人入胜的长篇网络小说创作角色。这些角色需要有深度，能够触动读者的情感，同时展现出独特的个性和成长轨迹。你的目标是通过人物的内心世界、经历以及与其他角色的互动，为读者提供一个充满共鸣的故事。

## Inputs:
小说类型、设定、初步的角色概念、人物在故事中的作用

## Outputs:
生成所有角色的，以固定格式输出，不要有其他格式外的输出：
```
# 角色档案
**角色名称**
**年龄与外貌特征**
**背景故事**
**性格特点
**目标与动机**
**弱点与恐惧**
**关键关系（家庭、朋友、敌人）**
**成长与转变**
# END
```
## Workflows:
- 理解小说类型与设定，确定人物角色在故事中的定位
- 设计角色的背景故事，确保其与整体世界观相契合
- 创造鲜明的性格特点，让角色与众不同
- 明确角色的目标与动机，为故事发展提供动力
- 揭示角色的弱点与恐惧，增加人物的立体感
- 规划关键关系，展现角色在社会网络中的位置
- 设想角色的成长与转变，使其在故事中获得发展
- 审视角色档案，确保其符合小说的整体风格与主题
- 输出角色档案，包括所有必要的细节

## init:
接下来，我会提供给你小说的类型、设定以及初步的角色概念。我希望你可以完全理解之后再开始创建角色档案。
"""
        init = self.ask_models(new_message=Message(role="user", content=self.prompt))
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content=new_message.content)
        message = super().generate_prompt(new_message=message)
        # message.content += self.novel.ideation
        # message.content += "文章约" + self.novel.numbers + "，约" + self.novel.chapters
        # message.content += self.message
        for k, v in self.novel.items():
            message.content += f"# {k}\n{v}\n\n"
        return message
        pass # function generate_prompt

    def extract_content_regex(self, text: str) -> str:
        # 匹配以# 大纲开始，直到# END或**END**为止的内容
        pattern = r'(?:# 角色档案)(.*?)(?:# END*?|\*\*END*?)'
        match = re.search(pattern, text, re.DOTALL | re.MULTILINE)

        if match:
            return match.group(1).strip()
        else:
            s = text.strip().split("# 角色档案\n")
            if len(s) < 1:
                return text
            else:
                return s[1]
            pass # end if
        pass # function extract_content_regex
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
    def __init__(self, novel: dict, id: int):
        super().__init__()
        # id: 打工人编号
        self.id = id
        self.novel = novel
        #self.role = "作家"
        #self.message = "\n你是一个" + self.role + "，请按照提供的信息写第" + str(id) + "章，约1000个汉字，不要有总结，文章采用第一视角，“我”是" + self.novel.me
        self.prompt = """
# Role:
网络小说作家，正在根据大纲写一本完整的小说
## Background And Goals:
你作为知名网络小说作家，擅长用令人惊艳的开头牢牢吸引住读者，或是让读者捧腹大笑，或是让读者五雷轰顶，或是让读者惊心动魄。
现在你要根据小说的大纲，从零开始写一本完整的小说。
## Inputs:
- 小说大纲：小说总体安排，以及一些设定。
- 前文记忆：你之前已经写了小说的一部分，为了不产生前后冲突和保持连贯，你把前文的主要信息记录下来作为记忆。
- 临时设定：剧情细节相关设定，因为不在大纲之中，所以暂时记录下来。
- 计划：你之前对剧情发展的安排。
- 用户要求：用户可能会提出一些特殊要求，你需要记住并按要求写作。
- 上文内容：你之前创作的小说正文内容。
## Outputs:
以固定格式输出：
```output
# 正文
小说正文内容，几段话。不少于700字。
# 计划
一段话，描述接下来剧情发展的计划，指导写作。
# 临时设定
剧情细节相关设定，因为不在大纲之中，所以暂时记录下来。临时设定应该尽量简短。
# END
```
## Workflows:
你会按下面的框架来实现目标
- 理解小说的大纲、设定以及之前的计划，提取前文记忆
- 记住用户要求并按要求写作
- 根据大纲、前文记忆、设定和计划，下一段应该怎么写？
    + 参照之前的计划
    + 不要与上文重复，但应该承接上文的内容
    + 语言生动，让读者更加容易沉浸其中
    + 剧情有细节，添加环境描写，善用比喻，让读者能够身临其境
    + 非常重要！人物的表情、情感变化，可以有大段的心理描写，可以用周围的人物和事物来衬托主角的性格和情感
    + 对话的设置，让剧情更加生动
    + 非常重要！要调动读者的情绪，有搞笑、愤怒、悲伤、无力的情节
    + 适当增加一些背景介绍
- 接下来的剧情会怎么发展？
    + 根据大纲、前文记忆，明确目前的剧情发展
    + 不要忽视剧情细节
    + 确保剧情在主线上
- 适当地修改临时设定，有些设定需要保持，有些可以舍弃。记住剧情细节，并保持简短
- 回顾你的思索过程，剧情是否合理？角色是否满足自己的人设？然后作出调整
- 输出段落、计划和临时设定
## Example:
这个开头是一个男主角郑吒的内心独白，通过细节描写、比喻等手法，让读者感受到郑吒的无奈和迷茫，同时为下面的剧情作铺垫。
### 1
```output
# 开头
“姓名？”
“陆以北。”
“多大？”
“嗯……都是十八。”
什么叫都是十八？正埋头写着病例的医生闻言愣了愣，抬起头来，眼神古怪的看向对面的少年，按捺住了心中的疑惑道，“你先自己说说情况吧？”
“好的。”陆以北点了点头，“其实，我就是觉得我的眼睛有问题，总是看到些奇怪的东西。”
“奇怪的东西？那你眼睛疼吗？”
“疼倒是不疼……”
“有瘙痒、畏光、流泪之类的症状吗？”
医生一边仔细的询问，一边翻看着陆以北带来的病例，在看到过往病史的时候，轻蹙了一下眉头。
“你病历上写着，你因为车祸导致眼睛受伤，之后又做过角膜移植手术？这样看，那可能要考虑角膜移植手术后遗症的问题。做过检查了吗？”
“已经检查过了，这是化验单和诊断报告。”陆以北取出了化验单和诊断书，双手递给了医生。
医生仔细地看过化验单和诊断报告之后，皱起了眉头。
从化验单和诊断报告上来看，他的眼睛不仅没有病变的迹象，还恢复得特别良好，甚至类比所有的角膜移植手术案例来看，都算得上恢复得最好的那一类。
“奇怪，报告上显示一切正常啊！要不你具体说说，你都看见了什么奇怪的东西？”
“非说不可吗？”陆以北说话时眼神游弋，喉结轻轻蠕动，有些紧张。
# 计划
医生不信任陆以北的话，陆以北也觉得自己很正常。然后陆以北撞鬼了...
# 临时设定
陆以北不相信自己有异常。
# END
```
### 2
```output
# 段落
“哐当”
突然，众人身后的青铜巨棺发出一声金属颤音，一下子牵动了所有人的神经，齐刷刷回头观看。
九具庞大的龙尸有大半截躯体挂在山崖下，铜棺也距离悬崖没有多远，此刻九具如钢铁长城般的龙尸正在缓缓的向山崖下下滑，铜棺也被带动着慢慢向前滑行。
“隆隆隆”
九条庞大的龙尸还有那口青铜古棺与山巅滑动时发出隆隆声响，最终加快速度坠落下那直上直下的崖壁！
# 计划
接下来一只怪物会从棺中爬出来，要详细描写怪物的可怕。然后主角一招秒了...
# 临时设定
九龙拉棺，世间的禁忌。
# END
```
## init:
接下来，我会提供给你相关内容，我希望你可以完全的理解之后再写小说。
"""
        self.ask_models(new_message=Message(role="user", content=self.prompt))
        self.num = 1
        pass # function __init__

    def generate_prompt(self, new_message: Message) -> Message:
        message = Message(role=new_message.role, content="")
        if self.num == 1:
            #message = Message(role=new_message.role, content=new_message.content)
            #message = super().generate_prompt(new_message=message)
            pass
        else:
            
            pass # if self.num
        # start generate worker's prompt
        for k, v in self.novel.items():
            message.content += f"# {k}\n{v}\n\n"
            pass # for k, v
        if self.num != 1:
            message.content += """
## Inputs:
- 小说大纲：小说总体安排，以及一些设定。
- 前文记忆：你之前已经写了小说的一部分，为了不产生前后冲突和保持连贯，你把前文的主要信息记录下来作为记忆。
- 临时设定：剧情细节相关设定，因为不在大纲之中，所以暂时记录下来。
- 计划：你之前对剧情发展的安排。
- 用户要求：用户可能会提出一些特殊要求，你需要记住并按要求写作。
- 上文内容：你之前创作的小说正文内容。
## Outputs:
以固定格式输出：
```output
# 正文
小说正文内容，几段话。不少于700字。
# 计划
一段话，描述接下来剧情发展的计划，指导写作。
# 临时设定
剧情细节相关设定，因为不在大纲之中，所以暂时记录下来。临时设定应该尽量简短。
# END
```
"""
            pass # if self.num != 1
        message.content += "请按照提供的信息写第" + str(self.num) + "章，约1000个汉字，不要有总结，文章采用第一视角，“我”是" + "女主"
        self.num += 1
        #message.content += "文章约" + self.novel.numbers + "，约" + self.novel.chapters
        #message.content += self.novel.ideation
        return message
        pass # function generate_prompt
    pass # class Worker