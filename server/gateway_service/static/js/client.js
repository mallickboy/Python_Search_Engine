console.log(
  "Version 3.0 of 'Python Search Engine' has been developed by Tamal Mallick.\n\n" +
  "This version builds upon the original 'Python Search Engine' project, which was created by Tamal Mallick, Sushanta Das, and Subham Manna."
);

// ----------------------
// Config & Root Elements
// ----------------------
const INPUT_BOX = document.getElementById("inputBox");
const SEARCH_BTN = document.getElementById("searchBtn");
const MAIN_DIV = document.getElementById("mainDiv");

const SEARCH_ENDPOINT = "/search";
const SEARCH_QUERY_PARAMETER_KEY = "q";
const EXIT_ENDPOINT = "/exit";
const GOOGLE_FAVICON_URL = "https://www.google.com/s2/favicons?domain=";

// ----------------------
// Cache
// ----------------------
const searchCache = {};  // { query: results }

// ----------------------
// Core Functions
// ----------------------
async function fetchSearchResults(query) {
  // Return cached results if present
  query = query.replace(/\s+/g, ' ').trim()  // compact query to reduce unnecessory req
  if (searchCache[query]) {
      console.log("Using cached results for:", query);
      return searchCache[query];
  }

  skeletonLoader();
  const queryUrl = `${SEARCH_ENDPOINT}?${SEARCH_QUERY_PARAMETER_KEY}=${encodeURIComponent(query)}`;
  console.log("Fetching:", queryUrl);
  const response = await fetch(queryUrl, { method: "GET" });
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const results = await response.json();
  searchCache[query] = results;  // store in cache
  return results;
}

function skeletonLoader() {
  MAIN_DIV.innerHTML = "";
  for (let i = 0; i < 5; i++) {
      const skeleton = `
      <br>
      <div class="search-result-element">       
        <div class="flex-container">
          <div> <a href="#" class="icon skeleton"> <img src="#"> </a> </div>
          <div>
            <div class="skeleton skeleton-domain"></div>
            <div class="skeleton skeleton-link"></div>
          </div>
        </div>
        <div class="heading-div skeleton skeleton-heading"></div>                  
        <div class="description skeleton skeleton-description"></div>
        <div class="description skeleton skeleton-description"></div>
      </div>
    `;
      MAIN_DIV.insertAdjacentHTML("beforeend", skeleton);
  }
}

function populateResults(results) {
  MAIN_DIV.innerHTML = "";
  if (!results || !results.length) {
      MAIN_DIV.innerHTML = "<p>No results found.</p>";
      return;
  }

  results.forEach(item => {
      const { title, link, desc } = item;
      const url = new URL(link);
      const domain = url.hostname;
      const decoratedLink = url.pathname.split("/").filter(Boolean)[0]
          ? `${domain}/${url.pathname.split("/").filter(Boolean)[0]}`
          : domain;

      const resultHTML = `
      <br>
      <div class="search-result-element">       
        <div class="flex-container">
          <div>
            <a href="${link}" class="icon" target="_blank">
              <img src="${GOOGLE_FAVICON_URL + domain}">
            </a>
          </div>
          <div>
            <div><a href="${link}" class="domain" target="_blank">${domain}</a></div>
            <div><a href="${link}" class="link" target="_blank">${decoratedLink}</a></div>
          </div>
        </div>
        <div class="heading-div">
          <a href="${link}" class="heading" target="_blank">${title}</a>
        </div>                  
        <div class="description">${desc.substring(0, 225)} ...</div>
      </div>
    `;
      MAIN_DIV.insertAdjacentHTML("beforeend", resultHTML);
  });
}

// ----------------------
// Event Handlers
// ----------------------
async function handleSearch(query, pushState = true) {
  query = query.replace(/\s+/g, ' ').trim() // compact query to reduce unnecessory req
  if (pushState) {
      const newUrl = `${window.location.pathname}?${SEARCH_QUERY_PARAMETER_KEY}=${encodeURIComponent(query)}`;
      window.history.pushState({ query }, "", newUrl);
  }

  if (!query) {
      // Clear results if no query
      MAIN_DIV.innerHTML = "";
      return;
  }

  try {
      const results = await fetchSearchResults(query);
      populateResults(results);
  } catch (err) {
      console.error("Error:", err);
      MAIN_DIV.innerHTML = `<p style="color:red;">Error fetching results: ${err.message}</p>`;
  }
}

// Enter key
INPUT_BOX.addEventListener("keydown", e => {
  if (e.key === "Enter") {
      e.preventDefault();
      handleSearch(INPUT_BOX.value);
  }
});

// Button click
SEARCH_BTN.addEventListener("click", () => {
  handleSearch(INPUT_BOX.value);
});

// Load query from URL params on first load
window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const q = params.get(SEARCH_QUERY_PARAMETER_KEY);
  if (q) {
      INPUT_BOX.value = q;
      handleSearch(q, false);
  }
});

// Handle browser back/forward
window.addEventListener("popstate", (event) => {
    const params = new URLSearchParams(window.location.search);
    const q = params.get(SEARCH_QUERY_PARAMETER_KEY) || "";
    INPUT_BOX.value = q;
    handleSearch(q, false); // false = don't push state again
});

// Notify server on exit
window.addEventListener("beforeunload", () => {
  navigator.sendBeacon(EXIT_ENDPOINT, JSON.stringify("Client left"));
});
