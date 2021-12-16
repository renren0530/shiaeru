FactoryBot.define do
  factory :user do
    nickname {Faker::Name.last_name}
    email {Faker::Internet.free_email}
    password {'Zoo1Zoo3'}
    password_confirmation {'Zoo1Zoo3'}
  end
end