"use strict"
console.log("UI.JS");
/******************************************************************************
 * Global constants
 */
BASE_API_URL = "http://localhost:5001/api/"
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
  console.log("clicked!");
  evt.preventDefault();
  const $evtTarget = $(evt.target);
  console.log("$evtTarget: ", $evtTarget);
  cafe_id = $evtTarget.data("cafe-id");
  console.log("cafe_id: ", cafe_id); 
  //make request to check to see if the user likes the cafe
  const params = new URLSearchParams({ "cafe_id": cafe_id })
  const response = await fetch(`${BASE_API_URL}likes?${params}`,
    { method: "GET" });
  resp_data = await response.json();
  console.log("resp_data: ", resp_data);
  //if false, make request to like cafe
  //if true, make request to unlike cafe

  // const response = await fetch(
  //   `${BASE_API_URL}like`,
  //   {
  //       method: "POST",
  //       body: JSON.stringify({"cafe_id": cafe_id}),
  //       headers: {
  //         "Content-Type": "application/json"},
  //   });
  // const data = await response.json();
}

$title.on("click", handleLikeClick);