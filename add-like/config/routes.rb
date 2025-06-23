Rails.application.routes.draw do
  # Define the route for Swagger UI in development environment
  if Rails.env.development?
    mount Rswag::Ui::Engine => '/api-docs-likes'
  end

  # Resources for 'posts' and nested 'likes' for creating likes on specific posts
  resources :posts do
    resources :likes, only: [:create]  # Nested route for creating a like for a specific post
  end
end
