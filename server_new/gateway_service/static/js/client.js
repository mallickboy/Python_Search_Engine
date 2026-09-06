console.log(
  "Version 3.0 of 'Python Search Engine' has been developed by Tamal Mallick.\n\n"
  // "This version builds upon the original 'Python Search Engine' project, which was created by Tamal Mallick, Sushanta Das, and Subham Manna."
);

// ----------------------
// Config & Root Elements
// ----------------------
const INPUT_BOX = document.getElementById("inputBox");
const SEARCH_BTN = document.getElementById("searchBtn");
const MAIN_DIV = document.getElementById("mainDiv");

const SEARCH_ENDPOINT = "/search";
const LLM_ENDPOINT = "/qna";
const SEARCH_QUERY_PARAMETER_KEY = "q";
const EXIT_ENDPOINT = "/exit";
const GOOGLE_FAVICON_URL = "https://www.google.com/s2/favicons?domain=";

// ----------------------
// Cache
// ----------------------
const searchCache = {};  // { query: results }
const llmCache = {};  // { query: response }

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

async function getLLMAnswer(query, rawResults) {
  try {
      // 1. Clean the data: only keep the 'desc' key and its value
      const cleanResponses = rawResults
          .filter(item => item.desc) // Safety check: skip items without a description
          .map(item => ({ desc: item.desc }));

      // 2. Post the request
      const response = await fetch(LLM_ENDPOINT, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              query: query,
              responses: cleanResponses
          }),
      });

      if (!response.ok) {
          throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      return data.answer;

  } catch (error) {
      console.error("LLM Request Failed:", error);
      return null;
  }
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
function cleanText(text) {
  return text
    .toLowerCase()
    .replace(/[\n\t]/g, " ")    // explicitly convert newline/tab → space
    .replace(/[^a-z\s]/g, "")   // keep only letters + spaces
    .replace(/\s+/g, " ")       // collapse multiple spaces
    .replace(/\s+/g, " ")       // collapse multiple spaces
    .trim();
}

async function handleSearch(query, pushState = true) {
  query = cleanText(query) // compact query to reduce unnecessory req
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

      await llm_qna(query, results)
  } catch (err) {
      console.error("Error:", err);
      MAIN_DIV.innerHTML = `<p style="color:red;">Error fetching results: ${err.message}</p>`;
  }
}

async function llm_qna(query, results) {
  // only cahnge after this line
  try {
    let llmAnswer;
    // 1. Create/Identify a UI container for the user to see the answer
    let aiContainer = document.getElementById("ai-answer-container");
    if (!aiContainer) {
        aiContainer = document.createElement("div");
        aiContainer.id = "ai-answer-container";
        // Basic styling for the UI box
        aiContainer.style.cssText  = `
        background:#F5FBFC;
        border-left:4px solid #4285f4;
        padding:15px;
        margin-top:2vh;
        margin-bottom:1vh;
        font-family:sans-serif;
        border-radius:12px;
        width:80%;
      `;
        MAIN_DIV.prepend(aiContainer);
    }

    aiContainer.innerHTML = "<em>✨ Gemini is generating an answer...</em>";

    // 2. Fetch the answer
    // Mapping to 'desc' helps stay within token limits and follows your requirement
    if (llmCache[query]) {
      console.log("Using cached results for LLM:", query);
      llmAnswer = llmCache[query];
    }
    else{
      llmAnswer = await getLLMAnswer(query, results.map(r => ({ desc: r.desc })));
      llmCache[query] = llmAnswer;
    }

    // 3. RESTORED: Your original QnA logs
    console.log(query);
    console.log(llmAnswer);

    // 4. Display in UI
    if (llmAnswer) {
        aiContainer.innerHTML = `<strong>AI Summary:</strong><br>${llmAnswer}`;
    } else {
        aiContainer.remove(); 
    }

  } catch (err) {
    console.error("Error:", err);
    // Clean up the UI container if the request fails
    const aiContainer = document.getElementById("ai-answer-container");
    if (aiContainer) aiContainer.remove();
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
