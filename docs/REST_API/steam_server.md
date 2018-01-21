**Steam Server**
----
   Checks if a Steam Server running on a specified IP/hostname and port is online

* **URL**

  /steam_server

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  `{'ip': '[ip/hostname]', 'port': '[port]'}`

* **Server Running Response:**

  * **Content:** `{ 'status': 'online' }`
 
* **Server Down Response:**

  * **Content:** `{ 'status': 'offline' }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'error' }`
  * Invalid IPv4 address / hostname or invalid port number
