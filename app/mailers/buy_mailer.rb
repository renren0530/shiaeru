class BuyMailer < ApplicationMailer
  def buy_mail(email, buy, returns, order_residense, nickname)
    @buy = buy
    @return = returns
    @order_residense = order_residense
    @nickname = nickname
    mail to: email, subject: '購入完了',
    from: '"しあえる" <noreply@yoursite.com>'
  end

  def order_mail(email, cart, order, order_residense, nickname)
    @cart = cart
    @order = order
    @order_residense = order_residense
    @nickname = nickname
    mail to: email, subject: '購入完了',
    from: '"しあえる" <noreply@yoursite.com>'
  end

end