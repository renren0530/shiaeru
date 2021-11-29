# アプリケーション名

!(https://user-images.githubusercontent.com/86912464/143829207-ee7eedb4-fa7e-48cf-a891-0a520db829e7.png)

# アプリケーション概要

実家の家業プロジェクトの一貫として、在庫処分兼自然保護のプロジェクトを立ち上げることになった。
それに伴いクラウドファンディングサイトに登録したが手数料が発生してしまい、思うように収益を上げることができなかった。
そのため手数料がかからないように自社のプロジェクトサイトを作成してコスト削減の目的でアプリ開発を実施した。

# URL

# テスト用アカウント

・資格保有ユーザー①
email : earth.r@i.softbank.jp
password : Zoo1Zoo3
資格保有ユーザー②
一般ユーザー
email : earth.rr@i.softbank.jp
password : Zoo1Zoo3


# 利用方法
・購入機能
  ログイン後、支援したいプロジェクトをクリックして詳細画面に以降。
  複数あるリターン商品から自分が支援したいリターンを選択すると、商品購入画面に移行。
  購入画面で自身の情報を入力して購入が完了すればトップページに移行する。
  マイページでは、自分が購入した商品履歴と購入金額の合計を確認することができる。

# 洗い出した要件
| 機能            | 目的   | 詳細    |   ストーリー｜
| ------------------ | ------ | ----------- |
| ユーザー管理機能 | 登録されたユーザーのみ使えるようにするため |購入履歴によってプロジェクトの寄付額を表示させる  |
| 購入機能 | 商品を購入させる | 在庫処分するはずの商品を購入してもらい、購入金額の一部を自然保護団体に寄付する  |
| 登録・編集・削除機能|プロジェクト、商品、ブランドなどを登録・編集・削除する| 今後プロジェクトや商品が変わったときに修正する|
| カート機能|商品をカートに入れる | 商品をカートに入れて後で確認したり、まとめて購入する|

# 実装した機能

# 工夫したポイント
・トップページをプロジェクトだけでなくブランドでも分けることで、ユーザーが購入したい商品を探しやすくした

# 実装予定の機能
・カートに入っている個数をjavascriptで自動更新できるようにする
・カートに商品を入れたときにヘッダーのカート部分に商品個数を表示できるようにする
・購入履歴に購入した日付を入力できるようにする

# データベース設計
![shiaeru](https://user-images.githubusercontent.com/86912464/143849424-1be4151b-6ce4-4219-8be8-990502706f73.png)


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
