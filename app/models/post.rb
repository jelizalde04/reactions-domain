class Post < ApplicationRecord
  # Establecer la conexión con la base de datos 'post_db'
  establish_connection :postdb

  # Definir la tabla de la base de datos
  self.table_name = 'Posts'

  # Definir la clave primaria
  self.primary_key = 'id'  # Asegúrate de que el id sea un UUID en la base de datos

  # Especificar los campos que se pueden asignar de manera masiva
  attr_accessor :content, :image, :likes, :comments

  # Definir los tipos de los campos para los castings
  def self.attribute_types
    {
      'id' => :uuid,
      'petId' => :uuid,
      'created_at' => :datetime,
      'updated_at' => :datetime
    }
  end
end
