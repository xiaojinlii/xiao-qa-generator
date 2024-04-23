from langchain_community.chat_models import ChatTongyi

from xiao_qa_generator.formatter.qa_json import QAJsonFormatter
from xiao_qa_generator.generator.batch import BatchGenerator
from xiao_qa_generator.generator.qa import QAGenerator
from xiao_qa_generator.generator.questions import QuestionsGenerator

if __name__ == '__main__':
    chat_model = ChatTongyi(dashscope_api_key="sk-xxx")
    chat_model.model_name = "qwen-plus"
    temperature = 2

    # 包含1个子问题
    # template_name = "prompt_questions_split/prompt_questions_split_one.txt"
    # generator = QuestionsGenerator(chat_model, template_name=template_name, temperature=temperature)
    # 包含2个子问题
    # template_name = "prompt_questions_split/prompt_questions_split_two.txt"
    # generator = QAGenerator(chat_model, template_name=template_name, temperature=temperature)
    # 包含3个子问题
    # template_name = "prompt_questions_split/prompt_questions_split_three.txt"
    # generator = QAGenerator(chat_model, template_name=template_name, temperature=temperature)
    # Prompt模板参数
    # input_variables = {
    #     "num_questions": 5
    # }

    # 多次生成后会有冗余问题，所以在提示词中增加有关的主题
    # 包含1个子问题
    # template_name = "prompt_questions_split/prompt_questions_split_one_topic.txt"
    # generator = QuestionsGenerator(chat_model, template_name=template_name, temperature=temperature)
    # 包含2个子问题
    # template_name = "prompt_questions_split/prompt_questions_split_two_topic.txt"
    # generator = QAGenerator(chat_model, template_name=template_name, temperature=temperature)
    # 包含3个子问题
    # template_name = "prompt_questions_split/prompt_questions_split_three_topic.txt"
    # generator = QAGenerator(chat_model, template_name=template_name, temperature=temperature)
    #
    # batch = BatchGenerator(generator, QAJsonFormatter)
    # output_dir = r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\batch_test"

    templates = [
        "prompt_questions_split/prompt_questions_split_one_topic.txt",
        "prompt_questions_split/prompt_questions_split_two_topic.txt",
        "prompt_questions_split/prompt_questions_split_three_topic.txt"
    ]
    topics = [
        "气候变化", "未来城市", "人工智能", "西游记", "水浒传", "三国演义", "红楼梦", "哈利波特", "天龙八部", "王者荣耀",
        "阅读习惯的养成", "李小龙", "刘德华", "周星驰", "黑洞", "物理学", "马尔代夫", "细胞", "区块链", "银河系",
        "高速公路", "软件开发", "红烧肉", "蜜蜂", "计算机", "iPhone", "android", "5G", "神经网络", "钢琴",
        "网络安全", "光合作用", "美国", "飞机", "网球比赛", "篮球比赛", "足球比赛", "台球", "氨基酸", "大熊猫",
        "星座运势", "火山喷发", "智能家居", "纳米技术", "能量守恒", "红薯", "番茄", "玉米", "大白菜", "大葱",
        "虚拟现实", "海洋保护", "垃圾回收", "太空探索", "可持续能源", "数字货币", "基因", "人机接口", "社交媒体", "量子计算"
    ]

    for i, template in enumerate(templates):
        if template == "prompt_questions_split/prompt_questions_split_one_topic.txt":
            generator = QuestionsGenerator(chat_model, template_name=template, temperature=temperature)
        else:
            generator = QAGenerator(chat_model, template_name=template, temperature=temperature)
        batch = BatchGenerator(generator, QAJsonFormatter)
        output_dir = fr"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\questions_split\{i+1}"

        for j, topic in enumerate(topics):
            input_variables = {
                "topic": topic,
                "num_questions": 5
            }
            batch.generate_batch(j+1, j+1, output_dir, **input_variables)
