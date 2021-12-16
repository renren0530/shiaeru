class BuysController < ApplicationController
  before_action :authenticate_user!, only: [:show, :buy, :create]

  def show
    @order_residence = OrderResidence.new
    @return = Return.find(params[:return_id])
    @buy = Buy.find(params[:id])
  end

  def buy
    @item = Item.find(params[:item_id])
    @return = Return.find(params[:return_id])
    @buy = Buy.new(return_id: @return.id, quantity: params[:quantity])
    if @buy.save
      redirect_to item_return_buy_path(@item.id, @return.id, @buy.id)
    else
      @item = Item.find(params[:item_id])
      render 'returns/show'
    end
  end

  def create
    @buy = Buy.find(params[:buy_id])
    @return = Return.find(params[:return_id])
    @order_residence = OrderResidence.new(order_params)
    
    if @order_residence.valid?
      pay_item
      @order_residence.save
      @order = Order.order(updated_at: :desc).limit(1)
      order_return = OrderReturn.new(order_id: @order.ids[0], return_id: @buy.return_id, quantity: @buy.quantity)
      order_return.save
      @email = current_user.email
      BuyMailer.buy_mail(@email,@buy,@return,@order_residence).deliver_now
      redirect_to buys_complete_path
    else
      render :show
    end
  end

  private

  def order_params
    params.require(:order_residence).permit(:postal_code, :item_prefecture_id, :city, :addresses, :building, :phone_number).merge(
      user_id: current_user.id, token: params[:token]
    )
  end

  def pay_item
    Payjp.api_key = ENV['PAYJP_SECRET_KEY']
    Payjp::Charge.create(
      amount: params[:sum],
      card: order_params[:token],
      currency: 'jpy'
    )
  end
end
