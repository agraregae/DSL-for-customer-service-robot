from typing import List, Tuple, Optional
from .dsl_lexer import DSLLexer, Token
from .ast import BotDef, IntentDef, SayAction, AskAction, SetAction, EndAction, Action


class DSLSyntaxError(Exception):
    pass


class DSLParser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # 工具方法区域 -----------------------------------------------------

    def _current(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None  # EOF

    def _accept(self, token_type: str) -> Optional[str]:
        """如果当前 token 类型匹配，就消耗它并返回值，否则返回 None"""
        tok = self._current()
        if tok is not None and tok[0] == token_type:
            self.pos += 1
            return tok[1]
        return None

    def _expect(self, token_type: str, msg: str = "") -> str:
        """必须匹配某种 token，否则抛出语法错误"""
        tok = self._current()
        if tok is None:
            raise DSLSyntaxError(f"Unexpected end of input; expected {token_type}. {msg}")
        if tok[0] != token_type:
            raise DSLSyntaxError(
                f"Unexpected token {tok[0]}({tok[1]}), expected {token_type}. {msg}"
            )
        self.pos += 1
        return tok[1]

    # 语法规则区域 -----------------------------------------------------

    def parse_bot(self) -> BotDef:
        """
        入口：bot "Name" { ... }
        """
        self._expect("BOT", "A script must start with 'bot'.")
        bot_name = self._expect("STRING", "Bot name must be a string.")

        self._expect("LBRACE", "Expected '{' after bot name.")

        intents = {}
        default_intent: Optional[IntentDef] = None

        while True:
            tok = self._current()
            if tok is None:
                raise DSLSyntaxError("Unexpected end of file, missing '}' for bot block.")

            if tok[0] == "RBRACE":
                # 结束 bot 块
                self._accept("RBRACE")
                break

            if tok[0] == "INTENT":
                intent_def = self._parse_intent()
                if intent_def.name in intents:
                    raise DSLSyntaxError(f"Duplicated intent name: {intent_def.name}")
                intents[intent_def.name] = intent_def
            elif tok[0] == "DEFAULT":
                if default_intent is not None:
                    raise DSLSyntaxError("Multiple default blocks are not allowed.")
                default_intent = self._parse_default()
            else:
                raise DSLSyntaxError(f"Unexpected token {tok}, expected INTENT or DEFAULT or '}}'.")

        return BotDef(name=bot_name, intents=intents, default_intent=default_intent)

    def _parse_intent(self) -> IntentDef:
        """
        intent "name" { actions... }
        """
        self._expect("INTENT", "Internal error: _parse_intent must start with INTENT token.")
        name = self._expect("STRING", "Intent name must be a string.")
        self._expect("LBRACE", "Expected '{' after intent name.")

        actions: List[Action] = []

        while True:
            tok = self._current()
            if tok is None:
                raise DSLSyntaxError("Unexpected end of file, missing '}' for intent block.")

            if tok[0] == "RBRACE":
                # 结束 intent 块
                self._accept("RBRACE")
                break

            actions.append(self._parse_action())

        return IntentDef(name=name, actions=actions)

    def _parse_default(self) -> IntentDef:
        """
        default { actions... }
        """
        self._expect("DEFAULT", "Internal error: _parse_default must start with DEFAULT token.")
        self._expect("LBRACE", "Expected '{' after default.")

        actions: List[Action] = []

        while True:
            tok = self._current()
            if tok is None:
                raise DSLSyntaxError("Unexpected end of file, missing '}' for default block.")

            if tok[0] == "RBRACE":
                self._accept("RBRACE")
                break

            actions.append(self._parse_action())

        # default 也用 IntentDef 来表示，不过 name 可以用固定名字
        return IntentDef(name="__default__", actions=actions)

    def _parse_action(self) -> Action:
        """
        支持的语句：
        - say "文本"
        - ask "问题" as var
        - set var = "value" 或 set var = otherVar
        - end
        """
        tok = self._current()
        if tok is None:
            raise DSLSyntaxError("Unexpected end of input inside block.")

        ttype, _ = tok

        if ttype == "SAY":
            self._accept("SAY")
            text = self._expect("STRING", "say 之后必须跟一个字符串。")
            return SayAction(text=text)

        elif ttype == "ASK":
            self._accept("ASK")
            prompt = self._expect("STRING", "ask 之后必须跟一个字符串问题。")
            self._expect("AS", "ask 指令后必须使用 'as' 指定变量名。")
            var_name = self._expect("IDENT", "变量名必须是标识符。")
            return AskAction(prompt=prompt, var_name=var_name)

        elif ttype == "SET":
            self._accept("SET")
            var_name = self._expect("IDENT", "set 之后必须跟变量名。")
            self._expect("EQUAL", "set 语句中缺少 '='。")

            # value 可以是字符串常量或变量名
            value_tok = self._current()
            if value_tok is None:
                raise DSLSyntaxError("set 语句缺少值。")
            if value_tok[0] not in ("STRING", "IDENT"):
                raise DSLSyntaxError("set 语句的值必须是字符串或标识符。")

            value = self._accept(value_tok[0])
            return SetAction(var_name=var_name, value=value)

        elif ttype == "END":
            self._accept("END")
            return EndAction()

        else:
            raise DSLSyntaxError(f"Unknown statement starting with token {tok}.")


# 对外提供的两个方便函数 -------------------------------------------

def parse_dsl(code: str) -> BotDef:
    """
    直接从字符串解析 DSL，返回 BotDef。
    """
    lexer = DSLLexer()
    tokens = lexer.tokenize(code)
    parser = DSLParser(tokens)
    return parser.parse_bot()


def parse_dsl_file(path: str) -> BotDef:
    """
    从 .dsl 文件解析，供 app.py 调用。
    """
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    return parse_dsl(code)
