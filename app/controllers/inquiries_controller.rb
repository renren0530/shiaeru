class InquiriesController < ApplicationController
  def new
    @inquiry = Inquiry.new
  end

  # 確認画面を作成する場合はこのような記述になるかと思います。
  # newアクションから入力内容を受け取り、
  # 送信ボタンを押されたらcreateアクションを実行します。
  def confirm
    @inquiry = Inquiry.new(inquiry_params)
    render :new if @inquiry.invalid?
  end

  # 実際に送信するアクションになります。
  # ここで初めて入力内容を保存します。
  # セキュリティーのためにも一定時間で入力内容の削除を行ってもいいかもしれません。
  def create
    @inquiry = Inquiry.new(inquiry_params)
    if @inquiry.save
      InquiryMailer.send_mail(@inquiry).deliver_now
      redirect_to done_path
    else
      render :new
    end
  end

  # 送信完了画面を使用する場合お使いください。
  def done
  end

  private

  def inquiry_params
    params.require(:inquiry)
          .permit(:email,
                  :name,
                  :phone_number,
                  :subject,
                  :message)
  end
end
