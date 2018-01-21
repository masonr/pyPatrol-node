**HTTP Response**
----
  Checks the HTTP response code of a given URL

* **URL**

  /http_response

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  `{'hostname': '[hostname]', 'redirects': '[true/false]'}`
  
  * *hostname* - URL or hostname of the website to check
  * *redirects* - Enables/disables the following of redirects (301/302)
  
* **HTTP Code Success Response:**

  * **Content:** `{ 'status': 'online', 'code': '200' }`
 
* **HTTP Code Failure Response:**

  * **Content:** `{ 'status': 'offline', 'code': '[HTTP Code]'  }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'offline', 'code': '404' }`
