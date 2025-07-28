
echo "Creating Image"
docker build . -t app_mcp_server:latest
echo "Stopping and removing existing container"
docker stop mcp_server
docker rm mcp_server
echo "Running new container"
docker run -d -p 8000:8000 -e WEATHER_API_KEY="3014397062237c10b9ca7d80bdb1a521" --name mcp_server app_mcp_server:latest
