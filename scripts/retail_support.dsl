bot "RetailSupport" {

  intent "greet" {
    say "你好，我是电商客服小助手，请问有什么可以帮你？"
  }

  intent "check_order_status" {
    say "好的，我可以帮你查询订单状态。"
    ask "请提供订单号：" as order_id
    # 在这里我们假装有个内部查询逻辑，这里用变量模拟
    set order_status = "已发货"
    say "订单 {{order_id}} 当前状态是：{{order_status}}。"
    end
  }

  intent "return_request" {
    say "明白，您想申请退货。"
    ask "请告诉我订单号：" as order_id
    ask "退货原因是什么？" as reason
    say "好的，我已为您提交退货申请，订单：{{order_id}}，原因：{{reason}}。"
    end
  }

  default {
    say "抱歉，我暂时没理解您的问题，可以换一种说法吗？"
  }
}
