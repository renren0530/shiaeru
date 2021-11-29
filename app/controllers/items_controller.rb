class ItemsController < ApplicationController

  def index
    @items = Item.all.order('created_at ASC')
    @brands = Brand.all.order('created_at ASC')

  end  

  def new
    @item = Item.new
  end  

  def create
    @item = Item.new(item_params)
    if @item.save
      redirect_to root_path
    else
      render :new
    end
  end  

  def show
    @item = Item.find(params[:id])
    @returns = Return.where(item_id: @item.id)
  end  

  def edit
    @item = Item.find(params[:id])
  end  

  def update
    @item = Item.find(params[:id])
    if @item.update(item_params)
     redirect_to root_path
    else
     render :edit
    end
  end

  def destroy
    @item = Item.find(params[:id])
    if @item.destroy
      redirect_to root_path
    end
  end

private
def item_params
  params.require(:item).permit(:item_name, :item_info, :image).merge(user_id: current_user.id)
end
end


