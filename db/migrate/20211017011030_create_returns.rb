class CreateReturns < ActiveRecord::Migration[6.1]
  def change
    create_table :returns do |t|
      t.string :return_name, null: false, default: ""
      t.text :return_info, null: false
      t.string :return_price, null: false
      t.string :return_donate, null: false
      t.references :item, null: false, foreign_key:true
      t.integer :brand_kinds_id, null: false
      t.timestamps
    end
  end
end
