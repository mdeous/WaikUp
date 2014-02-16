/*
    WaikUp API library
 */

var WaikUp = function(apiURL, apiKey) {
    "use strict";

    if (apiURL.substring(apiURL.length-1, apiURL.length) === "/") {
        // remove trailing slash, if any
        apiURL = apiURL.substring(0, apiURL.length-1);
    }

    var query = function(methodPath, method, data) {
        var endPoint = apiURL + methodPath;
        method = (typeof method === "undefined") ? 'GET' : method;
        data = JSON.stringify((typeof data === "undefined") ? {} : data);
        var response = $.ajax({
            type: method,
            url: endPoint,
            contentType: (method === "GET") ? "application/x-www-form-urlencoded" : "application/json",
            dataType: "json",
            headers: {"Auth": apiKey},
            success: function() {},
            error: function(xhr, err_desc, err_obj) {
                console.log("Failed to query "+endPoint+" ("+xhr.statusText+")");
            },
            data: data,
            async: false
        });
        return $.parseJSON(response.responseText);
    };

    var topFiveSubmitters = function() {
        return this.query('/users/top5submitters');
    };

    return {
        query: query,
        topFiveSubmitters: topFiveSubmitters
    };
};
