1) Create DockerFile
2) Create nginx.conf

docker build -t nginx-getpost .
docker run -d -p 8080:80 nginx-getpost

curl http://localhost:8080
# → You made a GET request!

curl -X POST http://localhost:8080
# → You made a POST request!

3 )Create containerregistry

az acr create --resource-group mytechresourcegroup --name bmdgmycontainerregistry --sku Basic

az acr login --name bmdgmycontainerregistry --resource-group mytechresourcegroup

docker tag nginx-getpost bmdgmycontainerregistry.azurecr.io/nginx-getpost:v1


docker push bmdgmycontainerregistry.azurecr.io/nginx-getpost:v1

4) Create AKS cluster 
## if you are subscription is not register with ContainerService run the below command to register 

az provider register --namespace Microsoft.ContainerService 

az provider show --namespace Microsoft.ContainerService --query "registrationState" 

az aks create --resource-group mytechresourcegroup --name bmdgAKSCluster --node-count 2 --node-vm-size standard_a2_v2 --enable-managed-identity --attach-acr bmdgmycontainerregistry  --generate-ssh-keys


az aks get-credentials --resource-group mytechresourcegroup --name bmdgAKSCluster

kubectl apply -f deployment.yaml

### To Create the service 
kubectl expose deployment myapp-deployment --port=80 --target-port=80 --name=myapp-service --type=LoadBalancer


##### Loadbalancer will create the public IP - we test using that url
curl -X POST http://135.13.15.165:80