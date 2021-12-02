
class UsersController < ApplicationController
  before_action :authenticate_user!, only: [:mypage] 
 
  def mypage
    @user = User.find(current_user.id)
    @orders = Order.where(user_id: current_user.id)
  end

  def pay
    
  end

end
