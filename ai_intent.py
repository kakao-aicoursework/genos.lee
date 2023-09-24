import os

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from ai_template import *

llm = ChatOpenAI(temperature=0.1, max_tokens=200, model="gpt-3.5-turbo")

intent_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template=read_prompt_template('./template/parse_intent.txt')
    ),
    output_key="intent",
    verbose=True,
)


def parse_intent(user_message: str) -> str:
    intent = intent_chain.run(dict(user_message=user_message))
    print(intent)
    return intent


if __name__ == '__main__':
    intent = parse_intent('싱크가 뭐야?')
    print(intent)
