@echo off

REM Run this file to start-up all docker containers developed for this project.
REM After running this file remember to wait untill container 'databases-startup' goes down! 

REM IMPORTANT: Only Windows can run this file!
REM            If on UNIX based system see: start_compose.sh

REM databases
docker compose -f app/databases/docker-compose.yml up -d --build

REM login authentication
docker compose -f app/login_register/docker-compose.yml up -d --build

REM modify and delete product 
docker compose -f app/controllers/admin/update_product/docker-compose.yml up -d --build

REM chatbot
docker compose -f app/processes/chatbot/docker-compose.yml up -d --build

REM frontend
docker compose -f app/frontend/docker-compose.yml up -d --build

REM orders history
docker compose -f app/controllers/customer/history_orders/docker-compose.yml up -d --build

REM create order 
docker compose -f app/controllers/customer/send_order/docker-compose.yml up -d --build

REM reccomendations
docker compose -f app/processes/reccomendation/docker-compose.yml up -d --build

REM order status change
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml up -d --build

REM warehouse stock management 
docker compose -f app/controllers/admin/magazyn/docker-compose.yml up -d --build
