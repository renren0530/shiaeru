class BrandsController < ApplicationController
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
    if @brand.delete
      redirect_to root_path
    end
  end

  private
def brand_params
  params.require(:brand).permit(:brand_name, :brand_info, :image)
end

end
