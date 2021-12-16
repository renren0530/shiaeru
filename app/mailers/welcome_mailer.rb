class WelcomeMailer < ApplicationMailer

  def send_when_signup(email,nickname)
    mail to: email, subject: '会員登録完了'
  end
end
