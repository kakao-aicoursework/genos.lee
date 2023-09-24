from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from ai_template import *
import requests
import json

llm = ChatOpenAI(temperature=1.0, max_tokens=4096, model="gpt-3.5-turbo-16k")

ask_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template=read_prompt_template('./template/ask_kakao_info.txt')
    ),
    output_key="answer",
    verbose=True,
)


def find_documents_from_chroma(question, size):
    resp = requests.get('http://127.0.0.1:9000/search?size=' + str(size) + '&query=' + question)
    if resp.status_code == 200:
        content = json.loads(resp.content)
        print(content['result'])
        return content['result']
    else:
        print('FAILED to query from chroma api')
        return []


def answer_for_kakao(question):
    docs = find_documents_from_chroma(question, 10)
    if len(docs) == 0:
        return '카카오와 관련된 정보를 찾을 수 없습니다.'

    answer = ask_chain.run(dict(related_documents=docs, user_question=question))
    print(answer)
    return answer


if __name__ == '__main__':
    answer_for_kakao('카카오 싱크 사용 과정을 알려줘')
