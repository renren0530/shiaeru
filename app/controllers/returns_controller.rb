class ReturnsController < ApplicationController
  before_action :authenticate_user!, except: [:show]
  before_action :set_action, only: [:new, :create, :edit, :update, :destroy]

  def new
  @return = Return.new
  end  

  def show
    @item = Item.find(params[:item_id])
    @return = Return.find(params[:id])
  end  

  def create
    @item = Item.find(params[:item_id])
    @return = Return.new(return_params)
    if @return.save
      redirect_to item_path(@item.id)
    else
      render :new
    end
  end

  def edit
    @return = Return.find(params[:id])
  end  

  def update
    @item = Item.find(params[:item_id])
    @return = Return.find(params[:id])

    if params[:return][:image_ids]
      params[:return][:image_ids].each do |image_id|
        image = @return.images.find(image_id)
        image.purge
      end
    end  
        
    if @return.update(return_params)
     redirect_to item_path(@item.id)
    else
     render :edit
    end
  end

  def destroy
    @item = Item.find(params[:item_id])
    @return = Return.find(params[:id])
    @return.destroy
    redirect_to item_path(@item.id)
  end

private
def return_params
  params.require(:return).permit(:return_name, :return_info, :return_price, :return_donate, :brand_kinds_id, images:[]).merge(item_id: params[:item_id])
end

def set_action
  unless user_signed_in? && (current_user.email == "earth_r@i.softbank.jp")
    redirect_to root_path
  end
end

end