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
  const cafe_id = $evtTarget.data("cafe-id");
  //make request to check to see if the user likes the cafe
  //if false, make request to like cafe
  //if true, make request to unlike cafe
  const cafeIsLiked = await checkIfCafeIsLiked(cafe_id);
  if (cafeIsLiked) {
    console.log('cafe is already liked');
    $toggleLikeBtn.text("Not Liked");
  } else {
    console.log('cafe not liked yet');
    await addLike(cafe_id);
    $toggleLikeBtn.text("Liked");
  }
}

/** checkIfCafeIsLiked: Makes API request to check if the current cafe is liked. 
 *    Accepts: cafe_id (int)
 *    Returns: true || false
*/
async function checkIfCafeIsLiked(cafe_id) {
  const params = new URLSearchParams({ "cafe_id": cafe_id })
  const response = await fetch(`${BASE_API_URL}likes?${params}`,
    { method: "GET" });
  const resp_data = await response.json();
  console.log("resp_data: ", resp_data);
  return resp_data.likes === true;
}

/** addLike: Makes API request to add the current cafe to the user's likes.
 *    Accepts: cafe_id (int)
 *    Returns: JSON {"liked": <cafe_id>}
 */
async function addLike(cafe_id) {
  const response = await fetch(
    `${BASE_API_URL}like`,
    {
      method: "POST",
      body: JSON.stringify({ "cafe_id": cafe_id }),
      headers: {
        "Content-Type": "application/json"
      },
    });
  const resp_data = await response.json();
  console.log("resp_data: ", resp_data);
  return resp_data;
}

$toggleLikeBtn.on("click", handleLikeClick);