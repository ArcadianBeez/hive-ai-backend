--orders--
id int unsigned auto_increment
primary key,
user_id int unsigned ,
order_status_id int(2) unsigned ,
created_at timestamp ,
updated_at timestamp ,
payment_id int unsigned ,
delivery_address_id int unsigned ,
whatever_address_id int unsigned ,
driver_id int unsigned ,
delivery_price double(8, 2)                 ,
billing_information_id int unsigned default 149 ,
comment_cancellation_id int unsigned ,
order_address_id int unsigned ,
restaurant_id int unsigned ,
delivery_discount double(8, 2) default 0.00 ,
preparation_time int default 0 ,
type varchar(10)  default 'NORMAL',
additional_transfer double(5, 2) default 0.00 ,
products_discount double(5, 2) default 0.00 ,
received smallint default 0 ,
app_version varchar(50)                  ,
constraint orders_user_id_foreign
foreign key (user_id) references prod.users (id)
foreign key (driver_id) references prod.users (id)
foreign key (restaurant_id) references prod.restaurants (id)
foreign key (payment_id) references prod.payments (id)

--users--
id int unsigned ,
name varchar(191) ,
email varchar(191) ,
password varchar(191) ,
api_token char(60)     ,
remember_token varchar(100) ,
created_at timestamp ,
updated_at timestamp ,
braintree_id varchar(191) ,
paypal_email varchar(191) ,
stripe_id varchar(191) ,
card_brand varchar(191) ,
card_last_four varchar(191) ,
trial_ends_at timestamp ,
device_token varchar(191) ,
phone_number longtext ,
restaurant_id int ,
platform varchar(10)

--restaurants--
id int ,
name varchar(191)
status varchar(191)

--payments--
id int unsigned auto_increment
primary key,
price double(8, 2) ,
description varchar(255) ,
user_id int unsigned ,
created_at timestamp ,
updated_at timestamp ,
status varchar(191) ,
method varchar(191) ,
observations varchar(500) 







