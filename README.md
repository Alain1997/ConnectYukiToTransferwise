This code has been written to connect Webflow to SellerActive.
Your website orders on Webflow will be retrieved and all required information to be able to send a customer their order will be sent to SellerActive.

In selleractive or in the code you can specify to which party you would like to send your order to be fulfilled, default in the code will be to send the order to Deliverr as this is our own 3PL warehouse that fulfills our orders but you could also choose Amazon FBA to fulfill your orders if you have inventory stocked there.

CODE WALKTHROUGH:
1. First the code scans your webflow website for new orders.
2. Once he has found a new order the code will sent this through to SellerActive to be fulfilled and the order will be stored in a database so it will not be fulfilled multiple times
3. If an order has already been fulfilled, then the code will start scanning SellerActive again but now for a tracking code to sent this through to webflow so the customer can start tracking their order.

