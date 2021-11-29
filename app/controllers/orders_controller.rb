class OrdersController < ApplicationController

  def index
    # @item = Item.find(params[:item_id])
    # @return = Return.find(params[:return_id])
    @order_residence = OrderResidence.new
    @cart = current_user.cart
  end  

  def show
    binding.pry
    @item = Item.find(params[:item_id])
    @return = Return.find(params[:id])
  end

  def create
    @cart = current_user.cart
    @order_residence = OrderResidence.new(order_params)
    if @order_residence.valid?
      pay_item
      @order_residence.save
      @order = Order.order(updated_at: :desc).limit(1)
      @cart.cart_returns.each do |cart_return|
        order_return = OrderReturn.new(order_id: @order.ids[0], return_id: cart_return.return_id, quantity: cart_return.quantity )
        order_return.save
        end

      @cart.destroy
      redirect_to root_path
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
    Payjp.api_key = ENV["PAYJP_SECRET_KEY"]
    Payjp::Charge.create(
      amount: params[:sum] ,
      card: order_params[:token],    
      currency: 'jpy'                 
    )
  end  
end

