class WelcomeMailer < ApplicationMailer

  def send_when_signup(email,nickname)
    @nickname = nickname
    mail to: email, subject: 'しあえる 登録完了のお知らせ'
  end
end
