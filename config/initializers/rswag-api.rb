# config/initializers/rswag-api.rb
Rswag::Api.configure do |config|
  # Ahora se usa openapi_root en lugar de swagger_root
  config.openapi_root = Rails.root.to_s + '/swagger'
end
