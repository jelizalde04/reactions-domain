require 'rails_helper'

# Configuración de swagger_helper.rb

RSpec.configure do |config|
  config.swagger_doxygen = {
    # Otros parámetros de configuración aquí
    info: {
      title: 'API LikeMS',
      version: 'v1'
    },
    securityDefinitions: {
      apiKey: {
        type: :apiKey,
        name: 'Authorization',
        in: :header,
        description: 'Token JWT'
      }
    },
    security: [
      { apiKey: [] }
    ]
  }
end
