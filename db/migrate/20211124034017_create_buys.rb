class CreateBuys < ActiveRecord::Migration[6.1]
  def change
    create_table :buys do |t|
      t.references :return, null: false, foreign_key:true
      t.integer :quantity, default: 0, null: false
      t.timestamps
    end
  end
end
