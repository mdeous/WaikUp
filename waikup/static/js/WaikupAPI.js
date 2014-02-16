/*
    WaikUp API library
 */

var WaikUp = function(apiURL, apiKey) {
    "use strict";

    if (apiURL.substring(apiURL.length-1, apiURL.length) === "/") {
        // remove trailing slash, if any
        apiURL = apiURL.substring(0, apiURL.length-1);
    }

    var query = function(methodPath, method, data, callback, async) {
        // handle default and required arguments
        if (typeof methodPath === "undefined") {
            console.log("Missing required argument: methodPath");
            return null;
        }
        var endPoint = apiURL + methodPath;
        method = (typeof method === "undefined") ? 'GET' : method;
        data = JSON.stringify((typeof data === "undefined") ? {} : data);
        callback = (typeof callback === "undefined") ? function(){} : callback;
        async = (typeof async === "undefined") ? true : async;

        var response = $.ajax({
            type: method,
            url: endPoint,
            contentType: (method === "GET") ? "application/x-www-form-urlencoded" : "application/json",
            dataType: "json",
            headers: {"Auth": apiKey},
            success: callback,
            error: function(xhr, err_desc, err_obj) {
                console.log("Failed to query "+endPoint+" ("+xhr.statusText+")");
            },
            data: data,
            async: async
        });
        if (async) {
            return $.parseJSON(response.responseText);
        }
        return null;
    };

    var topFiveSubmitters = function(callback) {
        this.query('/users/top5submitters', 'GET', {}, callback);
    };

    return {
        query: query,
        topFiveSubmitters: topFiveSubmitters
    };
};
