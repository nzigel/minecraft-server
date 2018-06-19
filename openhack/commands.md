kubectl get service minecraft-server --watch

kubectl get pods

az aks scale --resource-group=ohaus --name=ohAKSCluster --node-count 1

docker run -m 2G -d -p 25565:25565 -e EULA=TRUE -e MOTD="hello world" --name mc openhack/minecraft-server

docker container ls -a

docker rm 51ecf84ce68b

kubectl get service

kubectl get pods

az aks browse --resource-group ohaus --name ohAKSCluster

kubectl apply -f openhack/minecraft-server.yaml

kubectl get service minecraft-server --watch

az resource show --resource-group ohaus --name ohAKSCluster --resource-type Microsoft.ContainerService/managedClusters --query properties.nodeResourceGroup -o tsv

az storage account create --resource-group MC_ohaus_ohAKSCluster_australiaeast --name ohausstorageaccount --location australiaeast --sku Standard_LRS

kubectl apply -f openhack\azure-file-sc.yaml

kubectl apply -f openhack\azure-file-pvc.yaml

kubectl apply -f openhack\azure-pvc-files.yaml

kubectl describe pod mypod

kubectl get deployment

kubectl delete deployment minecraft-server

kubectl get services

kubectl delete services minecraft-server 

kubectl get storageclass

kubectl apply -f openhack/minecraft-server-persist.yaml

kubectl get pvc

kubectl get sc azurefile -o yaml

kubectl logs minecraft-serverv-669cb5bb84-cfd6v

kubectl apply -f openhack\azure-file-sc.yaml

kubectl exec -it minecraft-serverv-669cb5bb84-9x7tp ash

kubectl get sc azurefile -o yaml
