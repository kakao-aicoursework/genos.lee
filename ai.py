from ai_intent import parse_intent
from ai_kakao_info import answer_for_kakao
from ai_greeting import greeting
from ai_etc_info import answer_for_etc


def ask_to_bot(question):
    intent = parse_intent(question)

    if intent == '카정보':
        answer = answer_for_kakao(question)
    elif intent == '인사':
        answer = greeting(question)
    else:
        answer = answer_for_etc(question)
    return answer


if __name__ == '__main__':
    ask_to_bot('카카오 싱크 사용 과정을 알려줘')
