class BuyMailer < ApplicationMailer
  def buy_mail(soneemail, buy, returns, order_residense, nickname)
    @buy = buy
    @return = returns
    @order_residense = order_residense
    @nickname = nickname
    mail to: soneemail, subject: '購入通知(代引き)',
    from: '"しあえる" <noreply@yoursite.com>'
  end

  def cash_on_buy_mail(email, buy, returns, order_residense, nickname)
    @buy = buy
    @return = returns
    @order_residense = order_residense
    @nickname = nickname
    mail to: email, subject: '購入通知',
    from: '"しあえる" <noreply@yoursite.com>'
  end

  def buy_sonemails(soneemail, buy, returns, order_residense, nickname)
    @buy = buy
    @return = returns
    @order_residense = order_residense
    @nickname = nickname
    mail to: soneemail, subject: '購入するかも?',
    from: '"しあえる" <noreply@yoursite.com>'
  end

  def order_mail(soneemail, cart, order, order_residense, nickname)
    @cart = cart
    @order = order
    @order_residense = order_residense
    @nickname = nickname
    mail to: soneemail, subject: '購入通知(代引き)',
    from: '"しあえる" <noreply@yoursite.com>'
  end

  def cash_on_order_mail(email, cart, order, order_residense, nickname)
    @cart = cart
    @order = order
    @order_residense = order_residense
    @nickname = nickname
    mail to: email, subject: '購入通知',
    from: '"しあえる" <noreply@yoursite.com>'
  end

  def order_sonemails(soneemail, cart, order, order_residense, nickname)
    @cart = cart
    @order = order
    @order_residense = order_residense
    @nickname = nickname
    mail to: soneemail, subject: '購入するかも？',
    from: '"しあえる" <noreply@yoursite.com>'
  end

end