import os

from ai_memory import get_chat_history
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from ai_template import *

llm = ChatOpenAI(temperature=0.1, max_tokens=200, model="gpt-3.5-turbo")

greeting_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template=read_prompt_template('./template/greeting.txt')
    ),
    output_key="greeting",
    verbose=True,
)


def greeting(user_message: str) -> str:
    greeting = greeting_chain.run(dict(user_message=user_message,
                                       chat_history=get_chat_history()
                                       ))
    print(greeting)
    return greeting


if __name__ == '__main__':
    greeting = greeting('안녕?')
    print(greeting)
