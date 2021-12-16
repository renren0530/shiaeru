class BuyMailer < ApplicationMailer
  def buy_mail(email, buy, returns, order_residense)
    @buy = buy
    @return = returns
    @order_residense = order_residense
    mail to: email, subject: '購入完了'
  end

  def order_mail(email, cart, order, order_residense)
    @cart = cart
    @order = order
    @order_residense = order_residense
    mail to: email, subject: '購入完了'
  end

end