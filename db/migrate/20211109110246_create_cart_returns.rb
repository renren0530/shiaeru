class CreateCartReturns < ActiveRecord::Migration[6.1]
  def change
    create_table :cart_returns do |t|
      t.references :cart, null: false, foreign_key:true
      t.references :return, null: false, foreign_key:true
      t.integer :quantity, default: 0, null: false
      t.timestamps
    end
  end
end
