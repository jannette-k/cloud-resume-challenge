/**
 * script.js
 * ---------------------------------------------------------
 * Handles:
 *   1. Auto-updating the footer year.
 *   2. Calling the API Gateway endpoint (backed by Lambda +
 *      DynamoDB) to increment and display the visitor count.
 *
 * Replace API_URL below with your deployed API Gateway
 * invoke URL once the backend is live, e.g.:
 *   https://abcd1234.execute-api.eu-north-1.amazonaws.com/prod/visitor-count
 * ---------------------------------------------------------
 */

// ---- CONFIG -------------------------------------------------
const API_URL = "__API_URL__";// Replace with your API Gateway URL

// ---- FOOTER YEAR ---------------------------------------------
document.getElementById("year").textContent = new Date().getFullYear();

// ---- VISITOR COUNTER -------------------------------------------
async function updateVisitorCount() {
  const countEl = document.getElementById("visitor-count");

  try {
    const response = await fetch(API_URL, { method: "GET" });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();

    // Expecting the Lambda to return: { "count": <number> }
    countEl.textContent = data.count.toLocaleString();
  } catch (error) {
    console.error("Failed to fetch visitor count:", error);
    countEl.textContent = "unavailable";
  }
}

// Run on page load
updateVisitorCount();