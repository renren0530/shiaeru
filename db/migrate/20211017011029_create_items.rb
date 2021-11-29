class CreateItems < ActiveRecord::Migration[6.1]
  def change
    create_table :items do |t|
      t.string :item_name, null: false, default: ""
      t.text :item_info, null: false
      t.references :user, null: false, foreign_key:true
      t.timestamps
    end
  end
end
