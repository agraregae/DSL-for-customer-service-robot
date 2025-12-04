from chatbot.runtime import Interpreter, SessionState
from chatbot.intent_llm import DummyIntentRecognizer
from chatbot.dsl_parser import parse_dsl_file


def main():
    # 1. 解析 DSL 文件
    bot = parse_dsl_file("scripts/retail_support.dsl")

    # 2. 初始化意图识别器（先用 dummy）
    intent_recognizer = DummyIntentRecognizer(intents=list(bot.intents.keys()))

    # 3. 创建解释器和会话状态
    interpreter = Interpreter(bot, intent_recognizer)
    session = SessionState()

    print("欢迎使用 DSL 智能客服机器人，输入 'exit' 退出。")

    while True:
        user_text = input("用户: ")
        if user_text.strip().lower() == "exit":
            break

        replies = interpreter.handle_user_message(session, user_text)
        for r in replies:
            print("机器人:", r)


if __name__ == "__main__":
    main()
