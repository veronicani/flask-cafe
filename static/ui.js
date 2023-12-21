"use strict"

/******************************************************************************
 * Global constants
 */
const BASE_API_URL = "http://localhost:5001/api/"

/******************************************************************************
 * DOM elements
 */
const $toggleLikeBtn = $("#toggle-like-btn");

/******************************************************************************
 * checkIfCafeIsLiked: Makes API request to check if the current cafe is liked. 
 *    Accepts: cafe_id (int)
 *    Returns: true || false
*/
async function checkIfCafeIsLiked(cafeId) {
  const params = new URLSearchParams({ "cafe_id": cafeId })
  const response = await fetch(`${BASE_API_URL}likes?${params}`,
    { method: "GET" });
  const resp_data = await response.json();
  // console.log("resp_data: ", resp_data);
  return resp_data.likes === true;
}

/** toggleLike: Makes API request to add/remove the current cafe to/from the 
 * user's likes.
 *    Accepts: 
 *        cafe_id (int) - current cafe's id
 *        endpoint(str) - to add to the BASE_API_URL ("like" or "unlike")
 *    Returns: JSON 
 *        If endpoint is "/like" : {"liked": <cafe_id>} 
 *        If endpoint is "/unlike": {"unliked": <cafe_id>}
 */
async function toggleLike(cafeId, endpoint) {
  // console.log("endpoint: ", endpoint);
  const response = await fetch(
    `${BASE_API_URL}${endpoint}`,
    {
      method: "POST",
      body: JSON.stringify({ "cafe_id": cafeId }),
      headers: {
        "Content-Type": "application/json"
      },
    });
  const resp_data = await response.json();
  // console.log("resp_data: ", resp_data);
  return resp_data;
}

/** handleLikeClick: makes an AJAX call to the API to change the like/unlike
*  status, then changes the button to show updated status without refreshing
* the page.
*/
async function handleLikeClick(evt) {
  evt.preventDefault();

  const $evtTarget = $(evt.target);
  const cafeId = $evtTarget.data("cafe-id");

  const cafeIsLiked = await checkIfCafeIsLiked(cafeId);

  if (cafeIsLiked) {
    await toggleLike(cafeId, "unlike");
    $toggleLikeBtn.text("Not Liked");
  } else {
    await toggleLike(cafeId, "like");
    $toggleLikeBtn.text("Liked");
  }
}

$toggleLikeBtn.on("click", handleLikeClick);

