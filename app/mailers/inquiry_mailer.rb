class InquiryMailer < ApplicationMailer
  def send_mail(inquiry)
    @inquiry = inquiry
    
    mail to: "ENV["GOOGLE_MAIL_ADDRESS"]", subject: '【お問い合わせ】'
  end
end
