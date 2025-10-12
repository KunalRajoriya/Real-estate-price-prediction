function getBathValue() {
    // A more reliable way to get the value from the selected radio button
    var selectedBathroom = document.querySelector('input[name="uiBathrooms"]:checked');
    if (selectedBathroom) {
        return parseInt(selectedBathroom.value);
    }
    return -1; // Invalid Value
}

function getBHKValue() {
    // A more reliable way to get the value from the selected radio button
    var selectedBHK = document.querySelector('input[name="uiBHK"]:checked');
    if (selectedBHK) {
        return parseInt(selectedBHK.value);
    }
    return -1; // Invalid Value
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");

    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");

    // CORRECTED: Using a relative URL so it works on Render and your local machine
    var url = "/predict_home_price"; 

    console.log("Input values:", {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    });

    $.post(url, {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    }, function (data, status) {
        console.log("Response received:", data);
        if (data.estimated_price) {
            estPrice.innerHTML = `<h2>${data.estimated_price.toString()} Lakh</h2>`;
        } else {
            estPrice.innerHTML = `<h2>Error: ${data.error || "Unexpected response"}</h2>`;
        }
    }).fail(function (error) {
        console.error("Error in API call:", error);
        estPrice.innerHTML = `<h2>Error connecting to the server</h2>`;
    });
}


function onPageLoad() {
    console.log("document loaded");
    
    // CORRECTED: Using a relative URL here as well
    var url = "/get_location_names"; 

    $.get(url, function (data, status) {
        console.log("Got response for get_location_names request");
        if (data && data.locations) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty(); 
            $('#uiLocations').append(new Option("Choose a Location", "", true, true)); 

            for (var i = 0; i < locations.length; i++) {
                $('#uiLocations').append(new Option(locations[i], locations[i]));
            }
        } else {
            console.error("No locations found in the response");
        }
    }).fail(function () {
        console.error("Failed to fetch location names from API");
    });
}

window.onload = onPageLoad;