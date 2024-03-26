import json
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import openai
from langchain.chat_models import ChatOpenAI

from langchain.vectorstores import Milvus
from langchain.chains import RetrievalQA
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import gradio as gr
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferWindowMemory
from BCEmbedding import RerankerModel



app = Flask(__name__)
CORS().init_app(app)

openai_api_base = "http://localhost:8000/v1"
openai.api_key = "none"
llm = ChatOpenAI(
    model_name="chatglm3-6b",
    openai_api_base=openai_api_base,
    openai_api_key=openai.api_key,
    streaming=True,
    # 终端流式输出
    # callbacks=[StreamingStdOutCallbackHandler()],
    max_tokens=8000
)

class Chatbot:
    def __init__(self):
        embeddings = HuggingFaceEmbeddings(model_name="/home/madm/Downloads/WU_PYTHON/new/hquchatbot/src/model/m3e-base")
        self.vectorstore = Milvus.from_documents(
            documents='',
            embedding=embeddings,
            connection_args={"host": "10.8.13.118", "port": "19530", "db_name": "hquDemo"},
            collection_name="hqu_m3e",
        )
        # self.memory = ConversationBufferWindowMemory(k=3, return_messages=True)
        self.RerankerModel = RerankerModel(model_name_or_path="/home/madm/Downloads/WU_PYTHON/new/hquchatbot/src/model/rerankerModel/bce-reranker-base_v1")

    def get_prompt(self,user_input):
        docs = self.vectorstore.similarity_search(query=user_input, k=3)
        passages = []
        for doc in docs:
            passages.append(doc.page_content)
        rerank_results = self.RerankerModel.rerank(query=user_input, passages=passages)
        print(rerank_results["rerank_scores"][0])

        system_template1 = """
            你是华侨大学开发的校园服务AI助手。
            请你回答问题的时候，依据文档内容和聊天记录，一步步进行推理并得出结论，从而专业、完整地回答用户的问题并满足用户的要求。
            如果无法从中得到答案，请说"抱歉，根据已知信息无法回答该问题"，不允许在答案中添加编造成分。
            回答必须使用中文。
            上下文：{docs};
        """
        system_message_prompt1 = SystemMessagePromptTemplate.from_template(system_template1)
        human_template = "用户问题：{question}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        prompt_template1 = ChatPromptTemplate.from_messages([system_message_prompt1, human_message_prompt])
        prompt1 = prompt_template1.format_prompt(docs=rerank_results["rerank_passages"],
                                                 question=user_input)
        print(prompt1)
        system_template2 = """
            当别人问关于你的信息时,你需要回答你是华侨大学开发的校园服务AI助手。
            你需要使用中文,专业、完整的回答下面用户的问题并满足用户的要求。
        """
        system_message_prompt2 = SystemMessagePromptTemplate.from_template(system_template2)
        prompt_template2 = ChatPromptTemplate.from_messages([system_message_prompt2, human_message_prompt])
        prompt2 = prompt_template2.format_prompt(question=user_input)
        if rerank_results["rerank_scores"][0] > 0.5:
            result = llm.stream(prompt1)
            return result
        else:
            result = llm.stream(prompt2)
            return result
        # return outputs


@app.route('/')
def hello_world():
    result = llm.predict("你好")
    return result

@app.route('/demo', methods=['POST'])
def demo():
    argsJson = request.data.decode('utf-8')
    argsJson = json.loads(argsJson)
    question = argsJson['content']
    bot = Chatbot()
    result  = bot.get_prompt(question)
    def generate():
        for text in result:
            yield str(text)
            # print("ratio:", ratio)
    print(result)
    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route('/question', methods=['POST'])
def get_question():
    argsJson = request.data.decode('utf-8')
    argsJson = json.loads(argsJson)
    question = argsJson['content']
    print(question)
    # result = llm.predict(question)
    result = llm.stream(question)
    # print(type(result))

    def generate():
        for text in result:
            yield str(text)
            # print("ratio:", ratio)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")
    # return result

@app.route('/uploadFile',methods=['POST'])
def getFile():
    data = request.files
    file = data['file']
    # print(file.filename)
    file.save(f"接口文件/{file.filename}")
    return '收到文件'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5070)
