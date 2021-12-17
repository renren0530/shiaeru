class Return < ApplicationRecord
  belongs_to :item
  has_many_attached :images
  has_many :order_returns, dependent: :destroy
  has_many :buys, dependent: :destroy
  has_many :cart_returns

  validates :return_name, presence: true
  validates :return_info, presence: true
  validates :return_price, presence: true
  validates :return_donate, presence: true
  validates :images, presence: true
end
