docker build -t mcp-server .

docker run -p 8080:80 mcp-calculator:v3    

docker tag mcp-server bmdgmycontainerregistry.azurecr.io/mcp-server:v1

docker push bmdgmycontainerregistry.azurecr.io/mcp-server:v1


curl -X POST http://localhost:8080/mcp -H "Content-Type: application/json" -H "Accept: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\"}"

docker tag mcp-calculator bmdgmycontainerregistry.azurecr.io/mcp-calculator:v1

docker push bmdgmycontainerregistry.azurecr.io/mcp-calculator:v1

az acr update -n bmdgmycontainerregistry --admin-enabled true --resource-group mytechresourcegroup

for /f "delims=" %a in ('az acr credential show -n bmdgmycontainerregistry --resource-group mytechresourcegroup --query username -o tsv') do set ACRUSER=%a
for /f "delims=" %a in ('az acr credential show -n bmdgmycontainerregistry  --resource-group mytechresourcegroup --query passwords[0].value -o tsv') do set ACRPASS=%a

az containerapp env create --name mcp-env --resource-group mytechresourcegroup --location southindia

az containerapp create --name mcp-server --resource-group mytechresourcegroup --image bmdgmycontainerregistry.azurecr.io/mcp-calculator:v1 --environment mcp-env --ingress external --target-port 80 --registry-server bmdgmycontainerregistry.azurecr.io --cpu 0.5 --memory 1.0Gi


curl -X POST https://xxxxxxxxx.southindia.azurecontainerapps.io/mcp -H "Content-Type: application/json" -H "Accept: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\"}"
{"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"add","description":"","inputSchema":{"properties":{"a":{"title":"A","type":"integer"},"b":{"title":"B","type":"integer"}},"required":["a","b"],"title":"addArguments","type":"object"},"outputSchema":{"properties":{"result":{"title":"Result","type":"integer"}},"required":["result"],"title":"addOutput","type":"object"}}]}}