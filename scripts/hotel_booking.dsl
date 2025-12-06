bot "HotelBooking" {

  intent "greet" {
    say "您好，这里是酒店预订客服。"
  }

  intent "book_room" {
    say "我可以帮您预订客房。"
    ask "入住日期是？(例如：2025-12-20)" as checkin
    ask "离店日期是？(例如：2025-12-22)" as checkout
    ask "需要几间房？" as room_count
    say "好的，已为您预留 {{room_count}} 间房，入住：{{checkin}}，离店：{{checkout}}。"
    end
  }

  default {
    say "抱歉，目前我只支持预订客房相关问题。"
  }
}
