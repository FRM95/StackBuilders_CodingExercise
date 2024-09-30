import { validateParameters, fetchData, cacheData } from './fetch.js'

let lastFilter = null;

let originalDate = null;
let originalData = null;
let updatedData = null;

/* Display date of downloaded data */
const displayDate = (isoDate) => {
    const dateResult = document.querySelector(".date-results");
    if (dateResult != null) {
        dateResult.innerHTML = "";
        const spanDate = document.createElement("span");
        spanDate.textContent = `Date download: ${isoDate}`;
        dateResult.appendChild(spanDate);
    }
}

/* Display results of downloaded data */
const displayResults = (resultsArray) => {
    const results = document.querySelector(".data-results");
    if (results != null && resultsArray.length > 0){
        results.innerHTML = "";
        resultsArray.forEach(item => {
            const span = document.createElement("span");
            span.textContent = `${item["rank"]}. ${item["title"]} Score: ${item["score"]} Comments: ${item["comments"]}`;
            results.appendChild(span)
        })
    }
}

/* Remove message of fetch functions */
const removeMessage = () => {
    const dataMessage = document.querySelector(".data-message");
    if(dataMessage != null){
        dataMessage.innerHTML = "";
    }
}

/* Display message of fetch functions */
const displayMessage = (messageString) => {
    const dataMessage = document.querySelector(".data-message");
    if (dataMessage != null){
        dataMessage.innerHTML = "";
        dataMessage.textContent = messageString;
        setTimeout(removeMessage, 5000);
    }
}

/* Display Cache data from backend */
const displayCache = (resultsArray) => {
    const cacheResults = document.querySelector(".cache-results");
    if(cacheResults != null && resultsArray.length > 0){
        cacheResults.innerHTML = "";
        resultsArray.forEach(item => {
            const span = document.createElement("span");
            span.textContent = `Downloaded data: ${item["date"]} Filter applied: ${item["filter"]} Items crawled: ${item["data"].length}`;
            cacheResults.append(span);
        })
    }
}

/* Display the initial data from backend */
async function showInitialData(){
    const cache = await fetchData("display")
    if (cache instanceof Object){
        displayCache(cache);
    } else {
        displayMessage(cache);
    }
}

/* Main function */
function main(){

    /* Show original donwloaded data (30 entries) */
    const resetOriginal = document.querySelector(".reset");
    resetOriginal.addEventListener("click", () => {
        if(originalData != null && originalData.length > 0){
            displayResults(originalData);
        } 
        else {
            displayMessage("Unable to show original data, no data was downloaded")
        }
    })

    /* Button events to filter data */
    const filterButtons = document.querySelectorAll(".filter");
    filterButtons.forEach(button => { 
        button.addEventListener("click", () => {
            if(originalData != null && originalDate!= null){
                const data = button.getAttribute("data-value");
                const validParams = validateParameters({"filter_option": data});
                if(validParams instanceof Object){
                    fetchData("filter", validParams).then(response => {
                        if(response instanceof Array){
                            displayResults(response);
                            lastFilter = data;
                            updatedData = response;
                        } else {
                            displayMessage(response);
                        }
                    })
                }
            } else {
                displayMessage("Unable to filter data, no data was downloaded");
            }
        })
    })

    /* Button events to download data */
    const requestButton = document.querySelector(".crawl_data");
    requestButton.addEventListener("click", () => {
        fetchData("download").then(response => {
            if(response instanceof Object){
                originalData = response['crawl_data'];
                originalDate = response['crawl_date'];
                updatedData = response['crawl_data'];
                displayResults(response['crawl_data'])
                displayDate(response['crawl_date']);
                resetOriginal.disabled = false; 
                saveDataButton.disabled = false; 
                filterButtons.forEach(filter => filter.disabled = false);
            } else {
                displayMessage(response)
            }
        })
    })

    /* Button event to save data into backend cache */
    const saveDataButton = document.querySelector(".save");
    saveDataButton.addEventListener("click", async () => {
        if(originalDate != null && (updatedData != null && updatedData.length > 0)){
            const postParams = {"filter_option": lastFilter, "date" : originalDate}
            const saveToBackend = await cacheData("save", postParams, updatedData);
            displayMessage(saveToBackend);
            const displayBackendData = await fetchData("display");
            if(displayBackendData instanceof Object){
                displayCache(displayBackendData);
            } else {
                displayMessage(displayBackendData);
            } 
            originalDate = null
            originalData = null
            updatedData = null
            resetOriginal.disabled = true; 
            saveDataButton.disabled = true; 
            filterButtons.forEach(filter => filter.disabled = true);
            const infomessage = document.querySelector(".data-message-2");
            infomessage.textContent = "In order to apply more filters, request new data";
        } else {
            displayMessage("No data to save in cache");
        }
    });

    /* Call function to display last downloaded data and cached data */
    showInitialData();
}

/* Calling main function */
main();