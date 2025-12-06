from chatbot.dsl_parser import parse_dsl_file
from pprint import pprint

if __name__ == "__main__":
    bot = parse_dsl_file("scripts/retail_support.dsl")
    print("Bot name:", bot.name)
    print("Intents:", list(bot.intents.keys()))
    print("Default intent:", bot.default_intent.name if bot.default_intent else None)

    # 打印第一个 intent 的 actions 看看
    first_intent = next(iter(bot.intents.values()))
    print("First intent name:", first_intent.name)
    print("Actions:")
    pprint(first_intent.actions)
