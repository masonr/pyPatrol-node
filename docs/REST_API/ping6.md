**Ping**
----
  Pings (via IPv6) a specified IP/hostname

* **URL**

  /ping6

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **Data Params**

  `{'ip': '[ipv6_or_AAAA_hostname]'}`

* **Ping Success Response:**

  * **Content:** `{ 'status': 'online' }`
 
* **Ping Failure Response:**

  * **Content:** `{ 'status': 'offline' }`
  
* **Error Response:**

  * **Content:** `{ 'status': 'error' }`
  * Invalid IPv6 address or hostname
