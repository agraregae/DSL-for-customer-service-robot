bot "BankSupport" {

  intent "greet" {
    say "您好，这里是银行客服，请问需要办理哪方面业务？"
  }

  intent "check_balance" {
    say "我可以帮您查询账户余额。"
    ask "请告诉我您的账号后四位：" as account_tail
    set balance = "10234.50 元"
    say "账号尾号 {{account_tail}} 的当前余额为：{{balance}}。"
    end
  }

  intent "lost_card" {
    say "您要办理挂失，我来帮您。"
    ask "请确认挂失卡号后四位：" as card_tail
    say "好的，卡号尾号 {{card_tail}} 已经办理挂失，请您尽快携带证件到网点补办。"
    end
  }

  default {
    say "抱歉，我没理解您的问题，是查询余额还是挂失银行卡呢？"
  }
}
