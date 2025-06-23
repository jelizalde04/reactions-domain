
import { likeChannel } from "channels/like_channel";

document.addEventListener("DOMContentLoaded", () => {
 
  const postId = document.getElementById('post-id').dataset.postId;
  if (postId) {
    likeChannel(postId);
  }
});
