# WaikUp API Documentation

WaikUp provides a RESTful JSON API to programatically interact with the application.
The API only exposes user methods, no administrative action can be performed from it.

## Authentication

Every API calls require to be passed an `Auth` header holding the API key, which is 
available on the user's profile page.


## Errors

Errors are formatted the same way as regular responses, except they have an HTTP code
corresponding to the error type, with the error message in the JSON body's `message`
field.

Response body:
```json
{
    "message": "explanatory message about the error",
    "success": false
}
```


## Endpoints

### Links

* `GET /api/links?search=<str:search>&archived=<int:archived>` - Fetch links
    * `search` (optional, default: return all links) - Only fetch links
    matching `<search>` in their title, description, and URL
    * `archived` - (optional, default: 0) - Only fetch (un)archived links 
    (possible values: 0,1)

Response body:
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

* `POST /api/links` - Create a new link

Request body:
```json
{
  "url": "http://test.com/bla",
  "title": "blabla",
  "description": "some other link description",
  "category": "Cryptography"
}
```

* `url` (mandatory) - URL of the link to add
* `title` (mandatory) - Link title
* `description` (optional, default: "") - Link description
* `category` (optional, default: `DEFAULT_CATEGORY` setting) - Link category,
  the category must exist for the query to succeed

Response body:
```json
{
  "success": true,
  "linkid": 9
}
```

* `GET /api/links/<int:linkid>` - Fetch a specific link
    * `linkid` (mandatory) - ID of the link to fetch

Response body:
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

* `DELETE /api/links/<int:linkid>` - Delete a specific link (only allowed to the link owner and admins)
    * `linkid` (mandatory) - ID of the link to delete

Response body:
```json
{
  "linkid": 2,
  "success": true
}
```


### User profile

* `GET /api/profile` - Get the user profile

Response body:
```json
{
  "profile": {
    "id": 3,
    "email": "jerry@example.com",
    "first_name": "Jerry",
    "last_name": "Golay",
    "admin": true
  },
  "success": true
}
```


### Categories

* `GET /api/categories` - Get available categories

Response body:
```json
{
  "categories": [
    "System",
    "Security",
    "Networking",
    "Development",
    "Tools",
    "News",
    "Fun",
    "Other"
  ],
  "success": true
}
```
