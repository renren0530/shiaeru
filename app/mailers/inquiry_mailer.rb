class InquiryMailer < ApplicationMailer
  def send_mail(inquiry)
    @inquiry = inquiry
    mail to: "info@shiaeru.net", subject: '【お問い合わせ】'
    
  end
end
