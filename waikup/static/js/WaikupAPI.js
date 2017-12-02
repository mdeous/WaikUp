/*
 WaikUp API library
 */

var WaikUp = function(apiURL, apiKey) {
  "use strict";

  // remove trailing slash if any
  if (apiURL.substring(apiURL.length - 1, apiURL.length) === '/') {
    apiURL = apiURL.substring(0, apiURL.length - 1);
  }

  var query = function(endpoint, method, data, callback) {
    endpoint = apiURL + endpoint;
    var req = new XMLHttpRequest();
    req.open(method, endpoint, true);
    req.setRequestHeader('Auth', apiKey);
    req.setRequestHeader('Content-Type', 'application/json');
    req.onreadystatechange = function() {
      if (req.readyState === 4) {
        var resp = JSON.parse(req.responseText);
        if (req.status === 200) {
          if (resp.success) {
            callback(resp);
          } else {
            console.error(resp.message);
          }
        } else {
          console.error('Error querying ' + endpoint + ' (' + req.status.toString() + ')');
          console.error(resp.message);
        }
      }
    };
    req.send(data);
  };

  var listLinks = function(callback) {
    query('/links', 'GET', null, callback);
  };

  var addLink = function(url, title, description, category, callback) {
    var data = {
      url: url,
      title: title,
      description: description,
      category: category
    };
    query('/links', 'POST', JSON.stringify(data), callback);
  };

  var getLink = function(linkID, callback) {
    var endpoint = '/link/' + linkID.toString();
    query(endpoint, 'GET', null, callback)
  };

  var deleteLink = function(linkID, callback) {
    var endpoint = '/link/' + linkID.toString();
    query(endpoint, 'DELETE', null, callback)
  };

  var listCategories = function(callback) {
    query('/categories', 'GET', null, callback);
  };

  return {
    "listLinks": listLinks,
    "addLink": addLink,
    "getLink": getLink,
    "deleteLink": deleteLink,
    "listCategories": listCategories
  };
};
