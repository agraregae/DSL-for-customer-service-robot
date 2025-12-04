from typing import List


class DummyIntentRecognizer:
    '''
    关键词匹配的intent识别器，用于测试
    '''

    def __init__(self, intents: List[str]):
        self.intents = intents

    def recognize(self, user_text: str) -> str:
        text = user_text.lower()
        if "退货" in text or "return" in text:
            return "return_request"
        if "订单" in text or "order" in text:
            return "check_order_status"
        if "你好" in text or "hello" in text:
            return "greet"
        return "greet"
