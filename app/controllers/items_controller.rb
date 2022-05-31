class ItemsController < ApplicationController
  before_action :authenticate_user!, except: [:index, :show, :item_list, :project_list]
  before_action :set_action, only: [:new, :create, :edit, :update, :destroy]


  def index
    @items = Item.all.order('created_at ASC').limit(12)
    @brands = Brand.all.order('created_at ASC').limit(12)
    @returns = Return.all.order('created_at ASC').limit(12)
    @ukurainapage = Item.last(1)
    @ukuraina = Return.where(item_id: @ukurainapage[0][:id])
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
    redirect_to root_path if @item.destroy
  end

   def item_list
    @returns = Return.all.order('created_at ASC')
   end

   def project_list
    @items = Item.all.order('created_at ASC')
   end

  private

  def item_params
    params.require(:item).permit(:item_name, :item_info, :image).merge(user_id: current_user.id)
  end

  def set_action
    redirect_to root_path unless user_signed_in? && (current_user.email == 'earth_r@i.softbank.jp')
  end

 

end
