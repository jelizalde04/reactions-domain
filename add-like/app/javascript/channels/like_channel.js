import consumer from "./consumer";

const likeChannel = (postId) => {
  return consumer.subscriptions.create(
    { channel: "LikeChannel", post_id: postId },
    {
      received(data) {
        // Update the likes count on the page
        const likesCountElement = document.getElementById(`likes-count-${postId}`);
        if (likesCountElement) {
          likesCountElement.innerText = data.likes_count;
        }
      }
    }
  );
};

export { likeChannel };