class LikesController < ApplicationController
  before_action :authenticate_user!

  def create
    post = Post.find(params[:post_id])

    # Check if the user has already liked the post
    existing_like = Like.find_by(post_id: post.id, responsable_id: current_user.id)
    if existing_like
      return render json: { error: "You've already liked this post" }, status: :unprocessable_entity
    end

    # Create the like
    like = Like.create(post_id: post.id, responsable_id: current_user.id)
    if like.save
      # Update the like counter on the post
      post.increment!(:likes)

      # Broadcast the updated likes count to all clients subscribed to this post
      ActionCable.server.broadcast(
        "like_#{post.id}",
        { likes_count: post.likes }
      )

      render json: { message: "Like successfully created" }, status: :created
    else
      render json: { error: "Error creating like" }, status: :unprocessable_entity
    end
  end
end