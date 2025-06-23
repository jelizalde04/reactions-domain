
class LikeChannel < ApplicationCable::Channel
  def subscribed
    # The parameter params[:post_id] will be used to subscribe to a specific post
    stream_from "like_#{params[:post_id]}"
  end

  def unsubscribed
    # Cleanup can be done here if necessary
  end
end
