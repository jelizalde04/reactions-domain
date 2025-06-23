# app/controllers/concerns/authenticate_token.rb
module AuthenticateToken
  extend ActiveSupport::Concern

  included do
    before_action :authenticate_request  # Llamar al método de autenticación antes de cada acción
  end

  private

  def authenticate_request
    token = extract_token_from_header  # Extraer el token del encabezado de la solicitud

    if token.blank?
      render json: { error: 'Token no proporcionado.' }, status: :unauthorized and return
    end

    begin
      # Decodificar el token JWT utilizando la clave secreta y el algoritmo de verificación
      decoded_token = JWT.decode(token, ENV['JWT_SECRET'], true, algorithm: 'HS256')
      payload = decoded_token.first
      request.env['current_user_id'] = payload['userId']  # Asignar el ID del usuario al entorno de la solicitud
    rescue JWT::DecodeError, JWT::VerificationError
      render json: { error: 'Token inválido o expirado.' }, status: :forbidden
    end
  end

  def extract_token_from_header
    auth_header = request.headers['Authorization']
    return nil unless auth_header

    # Si el encabezado tiene el formato "Bearer <token>", extraer el token
    parts = auth_header.split(' ')
    parts.length == 2 && parts.first.downcase == 'bearer' ? parts.last : nil
  end
end
