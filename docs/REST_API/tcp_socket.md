**TCP Socket**
----
   Checks if a specified IP/hostname and port are listening for connections (TCP)

* **URL**

  /tcp_socket

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  `{'ip': '[ip/hostname]', 'port': '[port]'}`

* **Ping Success Response:**

  * **Content:** `{ 'status': 'online' }`
 
* **Ping Failure Response:**

  * **Content:** `{ 'status': 'offline' }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'error' }`
  * Invalid IPv4 address / hostname or invalid port number
