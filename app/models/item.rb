class Item < ApplicationRecord
  has_one_attached :image
  belongs_to :user
  has_many :returns, dependent: :destroy

  validates :item_name, presence: true
  validates :item_info, presence: true
  validates :image, presence: true



end
