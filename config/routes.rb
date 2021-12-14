Rails.application.routes.draw do

  root to: "items#index"
  devise_for :users, controllers: {
    omniauth_callbacks: 'users/omniauth_callbacks',
    registrations: 'users/registrations'
  }

  resources :items do
    resources :returns do
         resources :buys 
         post 'buys/:id' => 'buys#buy'
  end
end
  resources :orders



  get '/items/:item_id/returns/:return_id', to: 'returns#show', as: :item_return_id

  resources :inquiries, only: [:new, :create]
  post 'inquiries/confirm', to: 'inquiries#confirm', as: 'confirm'
  post 'inquiries/back', to: 'inquiries#back', as: 'back'
  get 'done', to: 'inquiries#done', as: 'done'

  resources :users do
  member do
    get 'mypage'
    end
   collection do
    get 'pay'
    get 'shiaeru'
    end 
  end  

  get '/my_cart' => 'carts#my_cart'
  post '/add_item' => 'carts#add_item'
  post '/update_item' => 'carts#update_item'
  delete '/delete_item' => 'carts#delete_item'
  get '/buys_complete' => 'buys#complete'


  resources :brands

end


