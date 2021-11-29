
class UsersController < ApplicationController
  
  def mypage
    @user = User.find(current_user.id)
    @orders = Order.where(user_id: current_user.id)
  end

  def indexpay
end

  def indexexchange
end

  def indexdelivery
end

end
