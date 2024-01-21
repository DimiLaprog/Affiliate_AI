# Affiliate_AI
 Program to Create affiliate adds


# Block Diagram

+-----------------------------------------------------+
|                       main()                        |
|                                                     |
|  +--------------+        +------------------------+  |
|  |  Load API    |        |  Load CSE ID and        |  |
|  |  Key from    |        |  Google Images Key      |  |
|  |  File        |        |  from Files             |  |
|  +------+-------+        +-------------+----------+  |
|         |                              |               |
|         v                              v               |
|  +------+---------------------+ +------+------------+|
|  | Build API Endpoint URL   | | Call Google Books  ||
|  | and Send GET Request     | | API to Get Book    ||
|  |                         | | Information        ||
|  +------------+------------+ +------+-------------+|
|               |                      |               |
|               v                      v               |
|  +------------+----------------------+-------------+|
|  | Process API Response (Check HTTP Status Code)    ||
|  |                                                  ||
|  +--------------------------+-----------------------+|
|                             |                        |
|                             v                        |
|  +--------------------------+-----------------------+|
|  | Loop over Books (Extract Title and Check Uniqueness||
|  | and Call Google Images API for Cover)              ||
|  +--------------------------+-----------------------+|
|                             |                        |
|                             v                        |
|  +--------------------------+-----------------------+|
|  | Call Google Images API to Search for Book Covers   ||
|  | using Google Custom Search API                     ||
|  +----------------------------------------------------+|
|                                                         |
+---------------------------------------------------------+
