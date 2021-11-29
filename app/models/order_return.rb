class OrderReturn < ApplicationRecord
  belongs_to :order
  belongs_to :return

end
