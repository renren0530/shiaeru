class CreateResidences < ActiveRecord::Migration[6.1]
  def change
    create_table :residences do |t|
      t.string :postal_code, null: false
      t.integer :item_prefecture_id, null: false
      t.string :city , null: false 
      t.string :addresses, null: false 
      t.string :building, null: false
      t.string :phone_number, null: false
      t.references :order, null: false, foreign_key:true
      t.timestamps
    end
  end
  
end
