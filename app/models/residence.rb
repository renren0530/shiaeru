class Residence < ApplicationRecord
  belongs_to :order
  belongs_to :item_prefecture

  extend ActiveHash::Associations::ActiveRecordExtensions
  belongs_to :item_prefecture
  validates :item_prefecture_id, numericality: { other_than: 1, message: "can't be blank" }
end
