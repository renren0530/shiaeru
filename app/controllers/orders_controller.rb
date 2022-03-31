class OrdersController < ApplicationController
  before_action :authenticate_user!, only: [:index, :create]

  def index
    # @item = Item.find(params[:item_id])
    # @return = Return.find(params[:return_id])
    @order_residence = OrderResidence.new
    @cart = current_user.cart
    if @cart.blank?
    redirect_to root_path
    end
  end

  def create
    @cart = current_user.cart
    @order_residence = OrderResidence.new(order_params)
    
    if @order_residence.valid?
      @order_residence.save
      @order = Order.order(updated_at: :desc).limit(1)
      settlement
      # @cart.cart_returns.each do |cart_return|
      #   order_return = OrderReturn.new(order_id: @order.ids[0], return_id: cart_return.return_id,
      #                                  quantity: cart_return.quantity)
      #   order_return.save
      # end
      @email = "info@shiaeru.net"
      BuyMailer.order_mail(@email, @cart, @order, @order_residence, current_user.nickname).deliver_now
      @cart.destroy
    else
      render :index
    end

  end


  def show
  end

  def update
  end

  private

  def order_params
    params.require(:order_residence).permit(:postal_code, :item_prefecture_id, :city, :addresses, :building, :phone_number).merge(
      user_id: current_user.id
      # token: params[:token]
    )
  end

  def settlement

    require "cgi"
    require "uri"
    require "net/https"
    require "rexml/document"
    require "open-uri"
    require 'active_support'
    require 'active_support/core_ext'
    require "rest-client"
    
    # proxy_port = -5000
    
    
    err_msg = nil
    
    # FORMで送信した内容をこのCGIで受け取るために、このCGIの名前を設定します。
    @my_self = ( $0.split("/") )[-1]
    
       # 契約番号(8桁) オンライン登録時に発行された契約番号を入力してください。
       contract_code = "72017390"

       item_name = ""
       sum = 0
       @cart.cart_returns.each do |cart_return| 
       item_name =  item_name + cart_return.return.return_name
       price = cart_return.return.return_price.to_i 
       quantity = cart_return.quantity.to_i 
       sum = price*quantity + sum
       end


      data = {
            "version" => "2",
                "contract_code" => contract_code,
                "user_id" => current_user.id,           
                "user_name" => current_user.nickname,  
                "user_mail_add" => current_user.email,
                "item_code" => @cart.id,       
                "item_name" => item_name,
                "order_number" => @order.ids[0],  
                "st_code" => "10000-0000-00000-00000-00000-00000-00000",
                "mission_code" => "1", 
                "item_price" => sum,     
                "process_code" => "1",                
                "xml" => "1",
                "character_code" => "UTF8"
      }
    
    
    # オーダー情報を送信した結果を格納する連想配列
    response = Hash.new
    
    # CGIオブジェクトの生成
    cgi = CGI.new( :accept_charset => 'UTF-8' )
    param = cgi.params
    
      RestClient.proxy = ENV["PROXIMO_URL"] 
      result = RestClient.post("https://secure.epsilon.jp/cgi-bin/order/receive_order3.cgi",data)
    
    
    
        # 結果の確認
        # if result.code == "200" 
          ##xml = REXML::Document.new(result.body)
          # p "============通った=============="
          xml = REXML::Document.new(( result.body.gsub("x-sjis-cp932","Shift_JIS")))
           # 文字コードをSJISとして読み込む(CP932はSJISの拡張なので基本はOK)
          xml.elements.each("Epsilon_result/result") do |element|
              element.attributes.each do |name, value|
                  response[name] = CGI.unescape(value)
                
              end
          end
      # else
      #     # イプシロンに対して接続に失敗
      #     err_msg =  "データの送信に失敗しました %s:%s<br><br>"%[result.code,result.headers]
        
      #     exit 1
      # end


    
      # result = 1 の場合、送信に成功
      if response["result"] == "1" then
          # recdirectがある場合
          if response.key?("redirect") then
              print cgi.header({"status" => "REDIRECT", "Location" => response["redirect"]})
              redirect_to response["redirect"]
          elsif response.key?("trans_code") then 
              print cgi.header({"status" => "REDIRECT", "Location" => confirm_url+("?trans_code=%d"%[response["trans_code"]] )})
              exit
          else
              # リダイレクトの指定なし、trans_codeがない場合は会員情報変更等
              result_page( response['result'] );
              exit
          end
      else
          # データ送信結果が失敗だった場合、オーダー入力画面に戻し、エラーメッセージを表示します。
          err_msg = "%s:%s"%[response["err_code"],response["err_detail"]]
          exit 1
      end
    
    end
end
