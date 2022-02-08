class BrandsController < ApplicationController
  before_action :authenticate_user!, except: [:show]
  before_action :set_action, only: [:new, :create, :edit, :update, :destroy]

  def new
    @brand = Brand.new
  end

  def create
    @brand = Brand.new(brand_params)
    if @brand.save
      redirect_to root_path
    else
      render :new
    end
  end

  def show
    @brand = Brand.find(params[:id])
    @returns = Return.all
  end

  def edit
    @brand = Brand.find(params[:id])
  end

  def update
    @brand = Brand.find(params[:id])
    if @brand.update(brand_params)
      redirect_to root_path
    else
      render :edit
    end
  end

  def destroy
    @brand = Brand.find(params[:id])
    redirect_to root_path if @brand.delete
  end

  def brand_list
    @brands = Brand.all.order('created_at ASC')
    @returns = Return.all.order('created_at ASC')
   end

  private

  def brand_params
    params.require(:brand).permit(:brand_name, :brand_info, :image)
  end

  def set_action
    redirect_to root_path unless user_signed_in? && (current_user.email == 'earth_r@i.softbank.jp')
  end
end
