from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from ai_template import *

llm = ChatOpenAI(temperature=1.0, max_tokens=4096, model="gpt-3.5-turbo-16k")

ask_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template=read_prompt_template('./template/ask_etc.txt')
    ),
    output_key="answer",
    verbose=True,
)


def answer_for_etc(question):
    answer = ask_chain.run(dict(user_question=question))
    print(answer)
    return answer


if __name__ == '__main__':
    answer_for_etc('3+1=?')
