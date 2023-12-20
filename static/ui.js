"use strict"

/******************************************************************************
 * Global constants
 */
const BASE_API_URL = "http://localhost:5001/api/"
/******************************************************************************
 * DOM elements
 */
const $toggleLikeBtn = $("#toggle-like-btn");
const $title = $("h1");
/******************************************************************************
 * handleLikeClick: makes an AJAX call to the API to change the like/unlike
 *  status, then changes the button to show updated status without refreshing
 * the page.
 */
async function handleLikeClick(evt) {
  evt.preventDefault();
  const $evtTarget = $(evt.target);
  const cafeId = $evtTarget.data("cafe-id");
  //make request to check to see if the user likes the cafe
  //if false, make request to like cafe
  //if true, make request to unlike cafe
  const cafeIsLiked = await checkIfCafeIsLiked(cafeId);
  if (cafeIsLiked) {
    console.log('cafe is already liked');
    // await addLike(cafeId);
    await toggleLike(cafeId, "unlike");
    $toggleLikeBtn.text("Not Liked");
  } else {
    console.log('cafe not liked yet');
    // await removeLike(cafeId);
    await toggleLike(cafeId, "like");
    $toggleLikeBtn.text("Liked");
  }
}

/** checkIfCafeIsLiked: Makes API request to check if the current cafe is liked. 
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
  console.log("endpoint: ", endpoint);
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
  console.log("resp_data: ", resp_data);
  return resp_data;
}

/** addLike: Makes API request to add the current cafe to the user's likes.
 *    Accepts: cafe_id (int)
 *    Returns: JSON {"liked": <cafe_id>}
 */
async function addLike(cafeId) {
  const response = await fetch(
    `${BASE_API_URL}like`,
    {
      method: "POST",
      body: JSON.stringify({ "cafe_id": cafeId }),
      headers: {
        "Content-Type": "application/json"
      },
    });
  const resp_data = await response.json();
  console.log("resp_data: ", resp_data);
  return resp_data;
}

/** removeLike: Makes API request to remove the current cafe from the user's
 *  likes.
 *    Accepts: cafe_id (int)
 *    Returns: JSON {"unliked": <cafe_id>}
 */
async function removeLike(cafeId) {
  const response = await fetch(
    `${BASE_API_URL}unlike`,
    {
      method: "POST",
      body: JSON.stringify({ "cafe_id": cafeId }),
      headers: {
        "Content-Type": "application/json"
      },
    });
  const resp_data = await response.json();
  console.log("resp_data: ", resp_data);
  return resp_data;
}

$toggleLikeBtn.on("click", handleLikeClick);

