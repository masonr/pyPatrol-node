**Certificates**
----
  Checks if a SSL certificate is valid or will expire within a specified threshold

* **URL**

  /cert

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  `{'hostname': '[hostname]', 'buffer': '[integer]'}`
  
  * *hostname* - hostname of the website to check
  * *buffer* - number of days to start warning about soon to expire certs
  
* **SSL Certificate Valid Response:**

  * **Content:** `{ 'status': 'valid', 'reason': 'valid' }`
     * If SSL certificate expires later than current date + *buffer*
 
     OR
     
  * **Content:** `{ 'status': 'valid', 'reason': 'expires soon' }`
     * If SSL certificate is valid but expires before the number of buffer days has passed
 
* **SSL Certificate Expired Response:**

  * **Content:** `{ 'status': 'invalid', 'reason': 'expired'  }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'error', 'reason': 'timeout' }`
     * If hit timeout trying to connect to the specified hostname
     
     OR
     
  * **Content:** `{ 'status': 'error', 'reason': 'error' }`
  
