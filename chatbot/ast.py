from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Action:
    pass


@dataclass
class SayAction(Action):
    text: str


@dataclass
class AskAction(Action):
    prompt: str
    var_name: str


@dataclass
class SetAction(Action):
    var_name: str
    value: str  # 先简单只支持字符串常量或变量名


@dataclass
class EndAction(Action):
    pass


@dataclass
class IntentDef:
    name: str
    actions: List[Action] = field(default_factory=list)


@dataclass
class BotDef:
    name: str
    intents: Dict[str, IntentDef] = field(default_factory=dict)
    default_intent: Optional[IntentDef] = None
