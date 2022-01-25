let data;
let returnData = (err, data) => {
    // Return data as points in the map
    if(err !== null) {
        console.error(`Error: ${err}`)
    } else {
        // data = JSON.stringify(data);
        console.log(data);        
    }
};

let getData = (lat, lng, callback) => {
    // getData for query
    let data = null;
    $.ajax({
        type: 'GET',
        url: 'https://data.police.uk/api/crimes-street/all-crime?lat='+lat+'&lng='+lng+'',
        success: (res) => {
            console.log("Sucess");
            callback(null, res);
        }
    });
};