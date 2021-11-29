# テーブル設計

## users テーブル

| Column             | Type   | Options     |
| ------------------ | ------ | ----------- |
| nickname           | string | null: false |
| email              | string | null: false, unique: true |
| encrypted_password | string | null: false |

### Association

- has_many :items
- has_many :orders


## items テーブル
 
| Column                      | Type       | Options     |
| ------------------          | ------     | ----------- |
| item_name                   | string     | null: false |
| item_info                   | text       | null: false |
| user                        | references |foreign_key:true, null: false |    

### Association

- belongs_to :user
- has_many :returns


## returns テーブル
 
| Column                      | Type       | Options     |
| ------------------          | ------     | ----------- |
| return_name                 | string     | null: false |
| return_info                 | text       | null: false |
| return_price                | integer    | null: false |
| return_donate               | integer    | null: false |
| item                        | references |foreign_key:true, null: false |     

### Association

- belongs_to :item
- has_one :order


## orders テーブル

| Column         | Type       | Options           |
| ------         | ---------- | -----------       |
| user           | references | foreign_key: true, null: false  |
| return         | references | foreign_key: true, null: false  |

### Association

- belongs_to :user
- belongs_to :return
- has_one :residence


## residences テーブル

| Column                | Type        | Options     |
| ------------------    | ------      | ----------- |
| postal_code           | string      | null: false |
| item_prefecture_id    | integer     | null: false |
| city                  | string      | null: false |
| addresses             | string      | null: false |
| building              | string      | null: false |
| phone_number          | string      | null: false |
| order           | references  | foreign_key: true, null: false  |

### Association

- belongs_to :order
