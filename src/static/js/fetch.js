/* Validate filter parameters of fetch function */
export const validateParameters = (objectParameters) => {
    const option = objectParameters['filter_option']
    if(option != undefined){
        if (option == "1" || option == "2"){
            return objectParameters
        } else {
            return 'Unknown filter value'
        }
    }
    return 'Invalid parameters'
}

/* Fetch function to get data fom the HTML parsing (crawl data) */
export async function fetchData(endpoint, params = null){
    try {
        let urlParams = "";
        if (params != null){
            urlParams += '?' + (new URLSearchParams(params)).toString();
        }
        const url = `/${endpoint}/` + urlParams;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Accept': 'application/json, text/html',
                }
            });
        if(!response.ok) {
            throw new Error('Network response was not ok');
        }
        const contentType = response.headers.get('content-type');
        if (contentType.includes('application/json')) {
            return await response.json();
        } else if (contentType.includes('text/html')) {
            return await response.text();
        }
    } catch (error) {
        console.error(error)
    }
}

/* Fetch function to get data fom backend cache */
export async function cacheData(endpoint, params, objectBody){
    try {
        let urlParams = "";
        urlParams += '?' + (new URLSearchParams(params)).toString();
        const url = `/${endpoint}/` + urlParams;
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(objectBody),
            headers: {
              'Content-Type': 'application/json',
                }
            });
        return await response.text();
    } catch (error) {
        console.error(error)
    }
}
