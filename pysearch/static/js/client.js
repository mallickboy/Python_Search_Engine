console.log(
    "Version 2.0 of 'Python Search Engine' has been developed by Tamal Mallick.\n\n" +
    "This version builds upon the original 'Python Search Engine' project, which was created by Tamal Mallick, Sushanta Das, and Subham Manna."
  );  
  
async function SearchAndGetResult(url, searchTopic) {
    skeletonLoader();
    searchTopic= searchTopic["searchTopic"];
    // console.log(searchTopic);
    const queryUrl = `${url}?q=${encodeURIComponent(searchTopic)}`;
    // window.history.pushState({searchTopic}, '', queryUrl);
    const response = await fetch(queryUrl, {
        method: "GET", 
        headers: {
            "Content-Type": "application/json"  // optional
        }
    });
    return await response.json();
}
window.addEventListener('DOMContentLoaded', function() {
    // Get the current query parameter from the URL (if any)
    const urlParams = new URLSearchParams(window.location.search);
    const searchTopic = urlParams.get('q');
    
    // If a search query exists, initiate the search
    if (searchTopic) {
        document.getElementById("inputBox").value = searchTopic;  // Optionally populate the search bar
        SearchAndGetResult("/search", searchTopic)
            .then(searchResult => {
                populateMainDiv(searchResult);  // Display search results
            })
            .catch(error => {
                console.error("Error:", error);  // Handle errors
            });
    }
});

function skeletonLoader() {
    const mainDivSelector = document.getElementById("mainDiv");
    mainDivSelector.innerHTML = "";
    
    for (let i = 0; i < 5; i++){
        const childDivElement = document.createElement("div");
        childDivElement.innerHTML = `<br>
            <div class="search-result-element">       
                <div class="flex-container">
                    <div> <a href="#" class="icon skeleton"> <img src="#"> </a> </div>
                    <div>
                        <div class="skeleton skeleton-domain">  </div>
                        <div class="skeleton skeleton-link">  </div>
                    </div>
                </div>
                <div class="heading-div skeleton skeleton-heading">
                    
                </div>                  
                <div class="description skeleton skeleton-description">                

                </div>            
                <div class="description skeleton skeleton-description">                

                </div>
            </div>
        `;
        mainDivSelector.appendChild(childDivElement);
    }     
}

var searchResult
const searchQuery = document.getElementById("inputBox");
searchQuery.addEventListener('keydown', function(event) {
    //  Enter (key code 13)
    if (event.keyCode === 13) {
        // prevent the default action (form submission, page reload
        event.preventDefault();
        console.log("Searching : ",searchQuery.value);
        SearchAndGetResult("/search",{ searchTopic:searchQuery.value})
        .then(searchResult => {
            populateMainDiv(searchResult)
        })
        .catch(error => {
            console.error("Error: ", error);
        });
    }
});
document.getElementById("searchBtn").onclick = function() {
    const searchTopic = document.getElementById("inputBox").value;
    console.log("Searching : ",searchTopic);
    SearchAndGetResult("/search",{ searchTopic:searchTopic})
     .then(searchResult => {
        populateMainDiv(searchResult)
     })
     .catch(error => {
        console.error("Error: ", error);
     });
};

window.addEventListener('beforeunload', function(event) {
    fetch("/exit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify("Client left")
    });
    // var ws = new WebSocket('ws://localhost:8080'); // Replace with your server's WebSocket URL
    // ws.onopen = function() {
    //     ws.send('TabClosed'); // Send a message to the server
    // };
});
/*const searchResult = [
    {
        "link": "https://www.javatpoint.com/array-in-java",
        "heading": "heading1",
        "description": "description1"
    },
    {
        "link": "https://www.geeksforgeeks.org/what-is-array",
        "heading": "heading2",
        "description": "description2"
    },
    {
        "link": "https://www.w3schools.com/java",
        "heading": "heading3",
        "description": "description3"
    }
]*/

function populateMainDiv(searchResult) {
    const mainDivSelector = document.getElementById("mainDiv");
    mainDivSelector.innerHTML = "";
    searchResult.map((item) => {
        title=item['title']
        link=item['link']
        desc = item['desc']
        const url = new URL(Object.values(item)[1]);
        const domainParts = url.hostname;
        const showDomain = domainParts || url.hostname;
        
        const baseURL = url.origin;

        const firstPathPart = url.pathname.split('/').filter(Boolean)[0] || '';

        // Construct a decorated display string:
        const decoratedLink = firstPathPart
        ? `${showDomain}/${firstPathPart}`
        : showDomain;

        //console.log(baseURL);
        /*const fullURL = new URL("favicon.ico", baseURL);
        console.log(fullURL);
        const faviconURL = fullURL.toString();
        console.log(faviconURL);*/

        const domain = baseURL.split("/");
        const googleFaviconGrabber = "https://www.google.com/s2/favicons?domain=";
        //console.log(googleFaviconGrabber+domain[2]);

        const childDivElement = document.createElement("div");


        childDivElement.innerHTML = `<br>
            <div class="search-result-element">       
                <div class="flex-container">
                    <div> <a href="${link}" class="icon" target="_blank"> <img src="${googleFaviconGrabber+domain[2]}"> </a> </div>
                    <div>
                        <div> <a href="${link}" class="domain" target="_blank"> ${domainParts} </a> </div>
                        <div> <a href="${link}" class="link" target="_blank"> ${decoratedLink} </a> </div>
                    </div>
                </div>
                <div class="heading-div">
                    <a href="${link}" class="heading" target="_blank"> ${title} </a>
                </div>                  
                <div class="description">   
                     ${desc.substring(0, 225) + " ..."}
                </div>
            </div>
        `;

        mainDivSelector.appendChild(childDivElement);
    })    
}