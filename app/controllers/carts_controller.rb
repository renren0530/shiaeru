class CartsController < ApplicationController
  before_action :authenticate_user!, only: [:my_cart, :add_item, :update_item, :delete_item]

  # カート内アイテムの表示
  def my_cart
    @cart = current_user.cart
  end

  # アイテムの追加
  def add_item
    cart = current_user.prepare_cart
    @cart_returns = cart.cart_returns.all
    @return = Return.find(params[:return_id])
    @cart_return = CartReturn.new(return_id: params[:return_id], cart_id: cart.id, quantity: params[:quantity])
    @cart_returns.each do |cart_return|
      next unless cart_return.return_id == @cart_return.return_id

      new_quantity = cart_return.quantity + @cart_return.quantity
      cart_return.update_attribute(:quantity, new_quantity)
      @cart_return.delete
    end
    @cart_return.save
    redirect_to my_cart_path
  end

  # アイテムの更新
  def update_item
    @cart_return = CartReturn.find(params[:cart_return_id])
    @cart_return.update(quantity: params[:quantity])
    @cart_return.delete if @cart_return.quantity == 0
    redirect_to my_cart_path
  end

  # アイテムの削除
  def delete_item
    CartReturn.destroy_by(return_id: params[:return_id])

    @cart = current_user.cart
    @cart.destroy if @cart.cart_returns.blank?
    redirect_to my_cart_path
  end
end
