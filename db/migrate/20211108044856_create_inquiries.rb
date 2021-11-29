class CreateInquiries < ActiveRecord::Migration[6.1]
  def change
    create_table :inquiries do |t|
      t.string :name, null: false
      t.string :email, null: false
      t.string :phone_number, null: false
      t.text :message, null: false
      t.timestamps
    end
  end
end
