from dataclasses import dataclass, field
from typing import Dict, Optional, List
from .ast import BotDef, IntentDef, SayAction, AskAction, SetAction, EndAction, Action


@dataclass
class SessionState:
    variables: Dict[str, str] = field(default_factory=dict)
    pending_ask: Optional[AskAction] = None
    current_intent: Optional[IntentDef] = None
    action_index: int = 0


class Interpreter:

    def __init__(self, bot: BotDef, intent_recognizer):
        self.bot = bot
        self.intent_recognizer = intent_recognizer

    def handle_user_message(self, session: SessionState, user_text: str) -> List[str]:
        '''
        输入用户文本，返回一组机器人回复（按顺序）。
        '''

        outputs: List[str] = []

        # 1. 如果有 pending_ask，说明上一轮在等待用户输入变量
        if session.pending_ask is not None:
            ask_action = session.pending_ask
            session.variables[ask_action.var_name] = user_text
            session.pending_ask = None
            # 继续执行当前 intent 后续动作
            outputs.extend(self._run_from_current_action(session))
            return outputs

        # 2. 没有 pending_ask，则先用 LLM 识别意图
        intent_name = self.intent_recognizer.recognize(user_text)
        intent = self.bot.intents.get(intent_name)

        if intent is None:
            # 使用 default
            intent = self.bot.default_intent

        session.current_intent = intent
        session.action_index = 0

        outputs.extend(self._run_from_current_action(session))
        return outputs

    def _run_from_current_action(self, session: SessionState) -> List[str]:
        outputs: List[str] = []
        intent = session.current_intent
        if intent is None:
            return outputs

        while session.action_index < len(intent.actions):
            action = intent.actions[session.action_index]
            session.action_index += 1

            if isinstance(action, SayAction):
                text = self._render_text(action.text, session.variables)
                outputs.append(text)

            elif isinstance(action, AskAction):
                # 输出问题，然后挂起
                text = self._render_text(action.prompt, session.variables)
                outputs.append(text)
                session.pending_ask = action
                break

            elif isinstance(action, SetAction):
                # 简化：直接把 value 当 literal 存
                session.variables[action.var_name] = self._render_text(action.value, session.variables)

            elif isinstance(action, EndAction):
                # 结束当前意图
                session.current_intent = None
                break

        return outputs

    @staticmethod
    def _render_text(template: str, variables: Dict[str, str]) -> str:
        # 简单模板渲染：替换 {{var}} 为实际值
        result = template
        for k, v in variables.items():
            result = result.replace("{{" + k + "}}", v)
        return result
