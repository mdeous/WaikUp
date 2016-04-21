# WaikUp API Documentation

WaikUp provides a RESTful API which allows to fetch/delete links and create new ones.

Request data must be passed as URL arguments for `GET` requests and url-encoded in the
request's body for `POST` requests.
 
 Responses are JSON objects.


## Authentication

All API calls require to be passed an `Auth` header holding the API key, which is available 
on your user information page.


## Endpoints

* `GET /api/links` - fetch all links

```json
{
    "links": [
        {
            "archived": false, 
            "author": "John Doe", 
            "category": "Development", 
            "description": "some link description", 
            "id": 1, 
            "submitted": "2016-04-11T22:26:16.545764", 
            "title": "some title", 
            "url": "http://blablablbgksrlnbgda.com"
        }, 
[...]
        {
            "archived": false, 
            "author": "Jerry Golay", 
            "category": "Cryptography", 
            "description": "some other link description", 
            "id": 6, 
            "submitted": "2016-04-18T23:34:48.045487", 
            "title": "blabla", 
            "url": "http://test.com/bla"
        }
    ], 
    "success": true
}
```

* `POST /api/links` - create a new link
    * `url`
    * `title`
    * `description` (optional, defaults to: "No description")
    * `category` (optional, defaults to the `DEFAULT_CATEGORY` setting value)

```json
{
    "success": true,
    "linkid": 9
}
```

* `GET /api/links/<int:linkid>` - fetch a specific link

```json
{
  "link": {
      "archived": false, 
      "author": "Jerry Golay", 
      "category": "Cryptography", 
      "description": "some other link description", 
      "id": 6, 
      "submitted": "2016-04-18T23:34:48.045487", 
      "title": "blabla", 
      "url": "http://test.com/bla"
  },
  "success": true
}
```

* `DELETE /api/links/<int:linkid>` - delete a specific link (only allowed to the link owner and admins)

```json
{
  "linkid": 2,
  "success": true
}
```


## Errors

Whenever an error occurs, the API returns a JSON object with the following structure:

```json
{
    "message": "explanatory message about the error",
    "success": false
}
```
