from chatbot.dsl_lexer import DSLLexer

dsl_code = """
bot "RetailSupport" {
  intent "greet" {
    say "你好，请问需要什么帮助？"
  }
}
"""

lexer = DSLLexer()
tokens = lexer.tokenize(dsl_code)

for t in tokens:
    print(t)