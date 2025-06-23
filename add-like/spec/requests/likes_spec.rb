# spec/requests/likes_spec.rb
require 'swagger_helper'

RSpec.describe 'Likes API', type: :request do
  path '/likes' do
    post 'Create a Like' do
      tags 'Likes'
      consumes 'application/json'
      parameter name: :Authorization, in: :header, type: :string, required: true, description: 'JWT Token'

      parameter name: :post_id, in: :query, type: :string, required: true, description: 'Post ID'

      response '201', 'Like created' do
        let(:Authorization) { 'Bearer some_valid_token' }
        let(:post_id) { 'some_post_id' }
        run_test!
      end

      response '422', 'Already liked' do
        let(:Authorization) { 'Bearer some_valid_token' }
        let(:post_id) { 'already_liked_post_id' }
        run_test!
      end
    end
  end
end
