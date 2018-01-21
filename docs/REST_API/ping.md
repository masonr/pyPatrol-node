**Ping**
----
  Pings (via IPv4) a specified IP/hostname

* **URL**

  /ping

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  `{'ip': '[ipv4_or_A_hostname]'}`

* **Ping Success Response:**

  * **Content:** `{ 'status': 'online' }`
 
* **Ping Failure Response:**

  * **Content:** `{ 'status': 'offline' }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'error' }`
  * Invalid IPv4 address or hostname
