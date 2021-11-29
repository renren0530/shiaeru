class OrderResidence
  include ActiveModel::Model
  attr_accessor :postal_code, :item_prefecture_id, :city, :addresses, :building, :phone_number, :user_id, :token

  with_options presence: true do
    validates :postal_code, format: { with: /\A[0-9]{7}\z/, message: 'is invalid. Include hyphen(-)' }
    validates :city
    validates :addresses
    validates :building
    validates :phone_number, format: { with: /\A[0-9]{10,11}+\z/ }
    validates :user_id
    validates :token
  end
  validates :item_prefecture_id, numericality: { other_than: 1, message: "can't be blank" }


  def save
    @order = Order.create(user_id: @user_id)
    Residence.create(postal_code: postal_code, item_prefecture_id: item_prefecture_id, city: city, addresses: addresses,
                     building: building, phone_number: phone_number, order_id: @order.id)
  end

end