class Order < ApplicationRecord
  belongs_to :user
  has_one :residence
  has_many :order_returns
end
