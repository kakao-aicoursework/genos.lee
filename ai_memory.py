from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
import os


def load_conversation_history(conversation_id: str):
    file_path = os.path.join('./chat_histories', f"{conversation_id}.json")
    return FileChatMessageHistory(file_path)


def log_user_message(history: FileChatMessageHistory, user_message: str):
    history.add_user_message(user_message)


def log_bot_message(history: FileChatMessageHistory, bot_message: str):
    history.add_ai_message(bot_message)


def get_chat_history(conversation_id: str = 'fa1010'):
    history = load_conversation_history(conversation_id)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="user_message",
        chat_memory=history,
    )

    return memory.buffer


def log(question, answer, conversation_id: str = 'fa1010'):
    history_file = load_conversation_history(conversation_id)
    log_user_message(history_file, question)
    log_bot_message(history_file, answer)
