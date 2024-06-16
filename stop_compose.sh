# !/bin/bash

# Run this file to stop all docker containers of this project.

# IMPORTANT: Only UNIX based systems can run this file!
#            If on Windows see: stop_compose.bat

# databases
docker compose -f app/databases/docker-compose.yml down

# login authentication
docker compose -f app/login_register/docker-compose.yml down

# modify and delete product 
docker compose -f app/controllers/admin/update_product/docker-compose.yml down

# chatbot
docker compose -f app/processes/chatbot/docker-compose.yml down

# frontend
docker compose -f app/frontend/docker-compose.yml down

# orders history
docker compose -f app/controllers/customer/history_orders/docker-compose.yml down

# create order 
docker compose -f app/controllers/customer/send_order/docker-compose.yml down

# reccomendations
docker compose -f app/processes/reccomendation/docker-compose.yml down

# order status change
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml down

# warehouse stock management 
docker compose -f app/controllers/admin/magazyn/docker-compose.yml down
