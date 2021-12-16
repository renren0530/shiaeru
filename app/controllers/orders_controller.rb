class OrdersController < ApplicationController
  before_action :authenticate_user!, only: [:index, :create]

  def index
    # @item = Item.find(params[:item_id])
    # @return = Return.find(params[:return_id])
    @order_residence = OrderResidence.new
    @cart = current_user.cart
  end

  def create
    @cart = current_user.cart
    @order_residence = OrderResidence.new(order_params)
    if @order_residence.valid?
      pay_item
      @order_residence.save
      @order = Order.order(updated_at: :desc).limit(1)
      @cart.cart_returns.each do |cart_return|
        order_return = OrderReturn.new(order_id: @order.ids[0], return_id: cart_return.return_id,
                                       quantity: cart_return.quantity)
        order_return.save
      end
      @email = current_user.email
      BuyMailer.order_mail(@email,@cart,@order,@order_residence).deliver_now
      @cart.destroy
      redirect_to buys_complete_path
    else
      render :index
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
