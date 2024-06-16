@echo off

REM Run this file to stop all docker containers of this project.

REM IMPORTANT: Only Windows can run this file!
REM            If on UNIX based system see: stop_compose.sh

REM databases
docker compose -f app/databases/docker-compose.yml down

REM login authentication
docker compose -f app/login_register/docker-compose.yml down

REM modify and delete product 
docker compose -f app/controllers/admin/update_product/docker-compose.yml down

REM chatbot
docker compose -f app/processes/chatbot/docker-compose.yml down

REM frontend
docker compose -f app/frontend/docker-compose.yml down

REM orders history
docker compose -f app/controllers/customer/history_orders/docker-compose.yml down

REM create order 
docker compose -f app/controllers/customer/send_order/docker-compose.yml down

REM reccomendations
docker compose -f app/processes/reccomendation/docker-compose.yml down

REM order status change
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml down

REM warehouse stock management 
docker compose -f app/controllers/admin/magazyn/docker-compose.yml down
