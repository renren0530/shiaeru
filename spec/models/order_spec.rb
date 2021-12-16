require 'rails_helper'

RSpec.describe OrderResidence, type: :model do
  before do
    @order_residence = FactoryBot.build(:order_residence)
    sleep 0.1
  end

  describe '商品購入' do
    context '商品購入できるとき' do
      it '空欄がすべて埋まっていれば登録できる' do
        expect(@order_residence).to be_valid
      end
      it 'buildingは空でも保存できること' do
        @order_residence.building = ''
        expect(@order_residence).to be_valid
      end
    end

    context '商品登録できないとき' do
      it 'postal_codeが空だと購入できない' do
        @order_residence.postal_code = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("Postal code can't be blank")
      end
      it 'item_prefecture_idが空だと購入できない' do
        @order_residence.item_prefecture_id = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("Item prefecture を入力してください")
      end
      it 'cityが空だと購入できない' do
        @order_residence.city = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("City can't be blank")
      end
      it 'addressesが空だと購入できない' do
        @order_residence.addresses = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("Addresses can't be blank")
      end
      it 'phone_numberが空だと購入できない' do
        @order_residence.phone_number = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("Phone number can't be blank")
      end
      it 'tokenが空だと購入できない' do
        @order_residence.token = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("Token can't be blank")
      end
      it 'item_prefecture_idが空だと購入できない' do
        @order_residence.item_prefecture_id = 1
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("Item prefecture を入力してください")
      end
      it 'postal_codeは「7桁」の半角形式でないと購入できない' do
        @order_residence.postal_code = '１１１１１１１'
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include('Postal code は(-)を含めないで半角で入力してください')
      end
      it 'postal_codeはハイフンがあると購入できない' do
        @order_residence.postal_code = '111-1111'
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include('Postal code は(-)を含めないで半角で入力してください')
      end
      it 'phone_numberは「9桁以下」だと購入できない' do
        @order_residence.phone_number = '111111111'
        @order_residence.valid?
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include('Phone number は(-)を含めないで半角で入力してください')
      end
      it 'phone_numberは「12桁以上」だと購入できない' do
        @order_residence.phone_number = '111111111111'
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include('Phone number は(-)を含めないで半角で入力してください')
      end
      it 'phone_numberは全角数値だと購入できない' do
        @order_residence.phone_number = '１１１１１１１１１１'
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include('Phone number は(-)を含めないで半角で入力してください')
      end
      it 'phone_numberはハイフンがあると購入できない' do
        @order_residence.phone_number = '111-1111-111'
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include('Phone number は(-)を含めないで半角で入力してください')
      end
      it 'ユーザーが紐付いていなければ購入できない' do
        @order_residence.user_id = ''
        @order_residence.valid?
        expect(@order_residence.errors.full_messages).to include("User can't be blank")
      end

    end
  end
end
