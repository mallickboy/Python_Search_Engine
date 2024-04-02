//Security
let public_key_server=null
fetch('/public-key').then(res=>res.json()).then(publicKey => {
            // Set the fetched public key to the encryptor object
            public_key_server=publicKey;
            console.log(publicKey)
    })

    class Knapsack {
        constructor() {}
    
        gcd(a, b) {
            while (b) {
                [a, b] = [b, a % b];
            }
            return a;
        }
    
        extendedGcd(a, b) {
            if (a == 0) {
                return [b, 0, 1];
            } else {
                const [g, y, x] = this.extendedGcd(b % a, a);
                return [g, x - Math.floor(b / a) * y, y];
            }
        }
    
        modInverse(a, m) {
            const [g, x] = this.extendedGcd(a, m).slice(0, 2);
            if (g !== 1) {
                return null;
            } else {
                return (x % m + m) % m;
            }
        }
    
        generateSuperIncreasingSequence(length) {
            let sequence = [Math.floor(Math.random() * 99) + 2];
            for (let i = 1; i < length; i++) {
                let nextElement = Math.floor(Math.random() * (2 * sequence.reduce((acc, val) => acc + val)) + sequence.reduce((acc, val) => acc + val)) + 1;
                sequence.push(nextElement);
            }
            return sequence;
        }
    
        privateKeyPublicKey(arrayLen, digitsNo) {
            let array = this.generateSuperIncreasingSequence(arrayLen);
            let minM = array.reduce((acc, val) => acc + val) + 1;
            let m = Math.floor(Math.random() * (10 ** digitsNo - array.reduce((acc, val) => Math.max(acc, val)))) + Math.max(array.reduce((acc, val) => Math.max(acc, val)), 10 ** (digitsNo - 1));
            let n;
            do {
                n = Math.floor(Math.random() * (m - 2)) + 2;
            } while (this.gcd(m, n) !== 1);
            let privateKey = n;
            let publicKey = array.map(element => (element * n) % m);
            this.privateKey = privateKey;
            this.modValue = m;
            this.array = array;
            this.publicKey = publicKey;
            return [privateKey, m, publicKey];
        }
    
        stringToBin(string) {
            let stringBin = '';
            for (let ch of string) {
                let ascii = ch.charCodeAt(0);
                let chBin = ascii.toString(2).padStart(8, '0');
                stringBin += chBin;
            }
            return stringBin;
        }
    
        breakIntoSumOf(target, arr) {
            function backtrack(start, path, target) {
                if (target === 0) {
                    result.push([...path]);
                    return;
                }
                if (target < 0 || start >= arr.length) {
                    return;
                }
                for (let i = start; i < arr.length; i++) {
                    if (i > start && arr[i] === arr[i - 1]) {
                        continue;
                    }
                    path.push(arr[i]);
                    backtrack(i + 1, path, target - arr[i]);
                    path.pop();
                }
            }
    
            let result = [];
            arr.sort((a, b) => a - b);
            backtrack(0, [], target);
            return result[0];
        }
    
        encryption(strBin, publicKey) {
            strBin = this.stringToBin(strBin);
            if (strBin.length % this.array.length !== 0) {
                console.log("GCD(string length,array length) must be 0 so that\n1.No element left in encryption\n2.No elements overproduced in decryption\n");
                return "Encryption Error";
            }
            let pubLen = publicKey.length;
            let i = 0,
                portionVal = 0,
                cy = '';
            for (let valBin of strBin) {
                valBin = parseInt(valBin);
                if (valBin) {
                    portionVal += valBin * publicKey[i];
                }
                i = (i + 1) % pubLen;
                if (i === 0) {
                    cy += portionVal + ' ';
                    portionVal = 0;
                }
            }
            if (i) {
                cy += portionVal + ' ';
            }
            return cy.trim();
        }
    
        decryption(cypherText) {
            let [privateKey, modVal, array] = [this.privateKey, this.modValue, this.array];
            let decryptionKey = this.modInverse(privateKey, modVal);
            let cypher = cypherText.split(' ');
           
            let text = '';
            for (let cy of cypher) {
                if(cy.length==0) continue
              
                let val = (parseInt(cy) * decryptionKey) % modVal;
                
                let comb = this.breakIntoSumOf(val, array);
                if (comb.length === 0 && val) {
                    console.log("ERR: decryption -> no combination found");
                }
                let decode = '';
                for (let element of array) {
                    if (comb.includes(element)) {
                        decode += '1';
                    } else {
                        decode += '0';
                    }
                }
                text += decode;
            }
            return this.binToText(text);
        }
    
        binToText(bin) {
            if (bin.length % 8 !== 0) {
                console.log("Not convertible");
                return;
            }
            let string = '';
            for (let start = 0; start < bin.length; start += 8) {
                string += String.fromCharCode(parseInt(bin.substr(start, 8), 2));
            }
            return string;
        }
    }
    
    // Usage
    let ks = new Knapsack();
    let [privateKey, modValue, publicKey] = ks.privateKeyPublicKey(8,8);
    // console.log("Private Key:", privateKey);
    // console.log("Mod Value:", modValue);
    // console.log("Public Key:", publicKey);
    
    // let plaintext = "Hello, world!";
    // let cypherText = ks.encryption(plaintext, publicKey);
    // console.log("Encrypted:", cypherText);
    
    // let decryptedText = ks.decryption(cypherText);
    // console.log("typeOfct:", typeof(cypherText));
    // x='1'
    // while (x !='0') {
    //     x=prompt("Plain text :")
    //     cy=ks.encryption(x, publicKey);
    //     alert(cy)
    //     text=ks.decryption(cy);
    //     alert(text)
    // }







async function postData(url, searchTopic) {
    skeletonLoader();
    const searchTopicEnc =  ks.encryption((JSON.stringify(searchTopic)), public_key_server);  
    console.log("Encrypted search",searchTopicEnc)
    // Create the request body with encrypted searchTopic and public key
    const body = JSON.stringify({
        searchTopic: searchTopicEnc,
        publicKey: publicKey
    });

    console.log(body)
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: body
    });

    return await response.text();
}
function decryptData(encryptedData) {
    

    
   
    const decryptedData = decryptor.decrypt(encryptedData);
    console.log("Decrypted data:", decryptedData);
    return decryptedData
}
function encryptData(sensitiveData) {
    
  

    const encryptedData = encryptor.encrypt(sensitiveData);
    console.log("Encrypted data:", encryptedData);
    return encryptedData

    // Now send the encryptedData to the server using AJAX, fetch, etc.
}
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

document.getElementById("searchBtn").onclick = function() {
    const searchTopic = document.getElementById("inputBox").value;

    postData("/submit",{ searchTopic:searchTopic})
     .then(searchResult => {
        console.log("search result before Decryption",searchResult)
        
        decryptedSearchResult= ks.decryption(searchResult) 

        decryptedSearchResult=JSON.parse(decryptedSearchResult)
        
        populateMainDiv(decryptedSearchResult)
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
    mainDivSelector.innerHTML = "";
    searchResult.map((item) => {
        title=item['title']
        link=item['link']
        desc = item['desc']
        const url = new URL(Object.values(item)[1]);
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
                    <div> <a href="${link}" class="icon"> <img src="${googleFaviconGrabber+domain[2]}"> </a> </div>
                    <div>
                        <div> <a href="${link}" class="domain"> ${domainParts[1]} </a> </div>
                        <div> <a href="${link}" class="link"> ${link} </a> </div>
                    </div>
                </div>
                <div class="heading-div">
                    <a href="${link}" class="heading"> ${title} </a>
                </div>                  
                <div class="description">   
                     ${desc.substring(0, 225) + " ..."}
                </div>
            </div>
        `;

        mainDivSelector.appendChild(childDivElement);
    })    
}