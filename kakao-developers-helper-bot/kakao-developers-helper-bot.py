"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# Import pynecone.
import openai
import os
from datetime import datetime

import pynecone as pc
from pynecone.base import Base

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage
)


# os.environ["OPENAI_API_KEY"] = ""


def load_data() -> str:
    path = './data/kakao_sync.txt'
    f = open(path, 'r')
    lines = f.readlines()
    return ''.join(lines)


data = load_data()

chat = ChatOpenAI(temperature=1.0, model_name='gpt-3.5-turbo-16k')
system_message = "assistant는 정보 제공 도우미로 동작한다. user의 아래 정보를 참고하여 질문에 답해라"
system_message_prompt = SystemMessage(content=system_message)

human_template = ("질문: {question}\n"
                  "정보: " + data + "\n"
                  )

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(llm=chat, prompt=chat_prompt)


def ask_to_bot(text):
    answer = chain.run(question=text)
    # answer = answer.replace('\n', '<br>')
    # print(answer)
    return answer


class Qa(Base):
    question: str
    answer: str
    created_at: str


class State(pc.State):
    """The app state."""

    question: str = ""
    qas: list[Qa] = []
    is_working: bool = False

    async def post(self):
        self.is_working = True
        yield
        if not self.question.strip():
            self.is_working = False
            return
        answer = ask_to_bot(self.question)
        self.qas = [
            Qa(
                question=self.question,
                answer=answer,
                created_at=datetime.now().strftime("%B %d, %Y %I:%M %p"),
            )
        ] + self.qas
        self.is_working = False


# Define views.


def header():
    """Basic instructions to get started."""
    return pc.box(
        pc.text("Kakao Developers Helper bot 🗺", font_size="2rem"),
        pc.text(
            "카카오 디벨로퍼스에 대해 궁금한 사항을 질문해보세요!",
            margin_top="0.5rem",
            color="#666",
        ),
    )


def down_arrow():
    return pc.vstack(
        pc.icon(
            tag="arrow_down",
            color="#666",
        )
    )


def text_box(text):
    return pc.text(
        text,
        background_color="#fff",
        padding="1rem",
        border_radius="8px",
    )


def qa(qa):
    return pc.box(
        pc.vstack(
            text_box(qa.question),
            down_arrow(),
            text_box(qa.answer),
            spacing="0.3rem",
            align_items="left",
        ),
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
    )


def smallcaps(text, **kwargs):
    return pc.text(
        text,
        font_size="0.7rem",
        font_weight="bold",
        text_transform="uppercase",
        letter_spacing="0.05rem",
        **kwargs,
    )


def output():
    return pc.box(
        pc.box(
            smallcaps(
                "Output",
                color="#aeaeaf",
                background_color="white",
                padding_x="0.1rem",
            ),
            position="absolute",
            top="-0.5rem",
        ),
        pc.text(State.output),
        padding="1rem",
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )


def index():
    """The main view."""
    return pc.container(
        header(),
        pc.input(
            placeholder="입력",
            on_blur=State.set_question,
            margin_top="1rem",
            border_color="#eaeaef"
        ),
        pc.button("Post", on_click=State.post, margin_top="1rem"),
        pc.vstack(
            pc.cond(State.is_working,
                    pc.spinner(
                        color="lightgreen",
                        thickness=5,
                        speed="1.5s",
                        size="xl",
                    ),),
            pc.foreach(State.qas, qa),
            margin_top="2rem",
            spacing="1rem",
            align_items="left"
        ),
        padding="2rem",
        max_width="600px"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="kakao-developers-helper-bot")
app.compile()
