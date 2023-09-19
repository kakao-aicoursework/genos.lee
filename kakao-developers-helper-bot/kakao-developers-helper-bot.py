"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# Import pynecone.
import openai
import os
from datetime import datetime

import pynecone as pc
from pynecone.base import Base


# openai.api_key = "<YOUR_OPENAI_API_KEY>"

def ask_to_bot(text):
    return text


class Qa(Base):
    question: str
    answer: str
    created_at: str


class State(pc.State):
    """The app state."""

    question: str = ""
    qas: list[Qa] = []

    @pc.var
    def output(self) -> str:
        if not self.question.strip():
            return ""
        return ask_to_bot(self.question)

    def post(self):
        if not self.question.strip():
            return
        self.qas = [
            Qa(
                question=self.question,
                answer=self.output,
                created_at=datetime.now().strftime("%B %d, %Y %I:%M %p"),
            )
        ] + self.qas


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
