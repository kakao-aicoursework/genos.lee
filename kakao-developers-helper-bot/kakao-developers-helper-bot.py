"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# Import pynecone.
from datetime import datetime

import pynecone as pc
from pynecone.base import Base
from ai import ask_to_bot


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
                    ), ),
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
