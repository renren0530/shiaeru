class WelcomeMailer < ApplicationMailer

  def send_when_signup(email,nickname)
    
    mail to: ENV['GOOGLE_MAIL_ADDRESS'], subject: '【お問い合わせ】'
  end
end
