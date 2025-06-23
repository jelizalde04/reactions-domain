class Responsible < ApplicationRecord
  # Establecer la conexión con la base de datos 'responsible_db'
  establish_connection :responsibledb

  # Definir la tabla de la base de datos
  self.table_name = 'Responsibles'  # Corrige el nombre de la tabla

  # Definir la clave primaria
  self.primary_key = 'id'

  # Especificar los campos que se pueden asignar de manera masiva
  attr_accessor :name, :email, :password, :contact, :avatar

  # Definir los tipos de los campos para los castings
  def self.attribute_types
    {
      'id' => :uuid,
      'created_at' => :datetime,
      'updated_at' => :datetime
    }
  end
end
