# !/bin/bash

# Run this file to start-up all docker containers developed for this project.
# After running this file remember to wait untill container 'databases-startup' goes down! 

# IMPORTANT: Only UNIX based systems can run this file!
#            If on Windows see: start_compose.bat

# databases
docker compose -f app/databases/docker-compose.yml up -d --build

# login authentication
docker compose -f app/login_register/docker-compose.yml up -d --build

# modify and delete product 
docker compose -f app/controllers/admin/update_product/docker-compose.yml up -d --build

# chatbot
docker compose -f app/processes/chatbot/docker-compose.yml up -d --build

# frontend
docker compose -f app/frontend/docker-compose.yml up -d --build

# orders history
docker compose -f app/controllers/customer/history_orders/docker-compose.yml up -d --build

# create order 
docker compose -f app/controllers/customer/send_order/docker-compose.yml up -d --build

# reccomendations
docker compose -f app/processes/reccomendation/docker-compose.yml up -d --build

# order status change
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml up -d --build

# warehouse stock management 
docker compose -f app/controllers/admin/magazyn/docker-compose.yml up -d --build
