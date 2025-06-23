Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins '*'  # Permite todos los orígenes
    resource '*', headers: :any, methods: [:get, :post, :put, :delete]
  end
end
