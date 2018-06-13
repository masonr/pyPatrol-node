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

  `{'hostname': '[hostname]', 'redirects': '[true/false]', 'check_string': '[true/false], 'keywords': '[string]'}`
  
  * *hostname* - URL or hostname of the website to check
  * *redirects* - Enables/disables the following of redirects (301/302)
  * *check_string* - Enables/disables searching for a specified text string on the page
  * *keywords* - The string to search for if check_string is enabled
  
* **HTTP Code Success Response:**

  * **Content:** `{ 'status': 'online', 'code': '200' }`

* **Keywords Not Found Response:**
  
  * **Content:** `{ 'status': 'offline', 'code': '200' }`
 
* **HTTP Code Failure Response:**

  * **Content:** `{ 'status': 'offline', 'code': '[HTTP Code]' }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'offline', 'code': '404' }`
