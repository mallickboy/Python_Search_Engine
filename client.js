async function postData(url, searchTopic) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(searchTopic)
    });

    return await response.json();
}

document.getElementById("searchBtn").onclick = function() {
    const searchTopic = document.getElementById("inputBox").value;

    postData("http://localhost:3000/data", {searchTopic})
     .then(searchResult => {
        populateMainDiv(searchResult)
     })
     .catch(error => {
        console.error("Error: ", error);
     });
};

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
    searchResult.map((item) => {
        const url = new URL(Object.values(item)[0]);
        const domainParts = url.hostname.split('.');

        const baseURL = url.origin;
        //console.log(baseURL);
        /*const fullURL = new URL("favicon.ico", baseURL);
        console.log(fullURL);
        const faviconURL = fullURL.toString();
        console.log(faviconURL);*/

        const domain = baseURL.split("/");
        const googleFaviconGrabber = "https://www.google.com/s2/favicons?domain=";
        //console.log(googleFaviconGrabber+domain[2]);

        const childDivElement = document.createElement("div");

        /*childDivElement.innerHTML = `<br>

            <a href="${Object.values(item)[0]}">            
            <div style="background: url(${googleFaviconGrabber+domain[2]}) center left no-repeat; padding: 5px 5px 5px 30px; text-decoration: none; font-color: black;">
            ${domainParts[1]} <br>
            ${Object.values(item)[0]}
            </div>
            <h5>${Object.values(item)[1]}</h5>
            </a>
            ${Object.values(item)[2]}
        `;*/

        childDivElement.innerHTML = `<br>
            <div class="search-result-element">       
                <div class="flex-container">
                    <div> <a href="${Object.values(item)[0]}" class="icon"> <img src="${googleFaviconGrabber+domain[2]}"> </a> </div>
                    <div>
                        <div> <a href="${Object.values(item)[0]}" class="domain"> ${domainParts[1]} </a> </div>
                        <div> <a href="${Object.values(item)[0]}" class="link"> ${Object.values(item)[0]} </a> </div>
                    </div>
                </div>
                <div class="heading-div">
                    <a href="${Object.values(item)[0]}" class="heading"> ${Object.values(item)[1]} </a>
                </div>                  
                <div class"description">   
                    ${Object.values(item)[2]}
                </div>
            </div>
        `;

        mainDivSelector.appendChild(childDivElement);
    })    
}