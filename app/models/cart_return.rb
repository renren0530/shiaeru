class CartReturn < ApplicationRecord
  belongs_to :return
  belongs_to :cart

extend ActiveHash::Associations::ActiveRecordExtensions
belongs_to :item_quantity
end
