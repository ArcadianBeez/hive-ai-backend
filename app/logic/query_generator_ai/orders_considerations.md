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
when the query question for gain of a person thats refer to driver 
when the query question for gain of a store or similar is refer to restaurant
when the query question includes sales for restaurants ever verify restaurants.status is 1
when the query contains some related of payment method should make join with payments

payments.method is
- TRANSFER
- CASH 
- CARD

when the query contains some related of gain of restaurant or store use payments.price 
when the query contains some related of commission use (payments.price * restaurants.commission_percentage)/100 and round 2 decimals