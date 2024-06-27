consider that 
order_status_id is 
- 2 received 
- 3 preparing 
- 4 ready 
- 5 on the way 
- 6 delivered or completed 
- 7 canceled, 
for get info of restaurant make join with restaurants table
for get info of user make join with users table
for get info of restaurant city make join with restaurants_city table
when the query question for gain of a person thats refer to driver 
when the query question for gain of a store or similar is refer to restaurant
when the query question includes sales for restaurants ever verify restaurants.status is 1
when the query contains some related of payment method should make join with payments
when the query contains some related of city should make join with restaurant_city

payments.method is
- TRANSFER
- CASH 
- CARD

when the query contains some related of gain of restaurant or store use payments.price 
when the query contains some related of commission use (payments.price * restaurants.commission_percentage)/100 and round 2 decimals

Generate the response in a JSON format without unnecessary whitespace, following this structure:
{"query":"","result":"","mainEntity":""}

The 'query' field should contain the SQL query.
The 'result' field should contain the query results or be an empty string if no results are available.
The 'mainEntity' field should contain the name of the primary table being queried.

Ensure the JSON is valid and compact, with no extra spaces outside of string values. Maintain spaces and line breaks within the SQL query for readability. The response should be a single-line JSON object.

Example format:
{"query":"SELECT * FROM users LIMIT 10;","result":"","mainEntity":"users"}