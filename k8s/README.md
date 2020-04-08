Steps for converting docker compose files to kubernetes 

`$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml config > kompose.yml`

Some manual correction

`$ kompose -f kompose.yml convert`

Some manual correction

Create `newsgac.yourdomain` domain in DNS:
```bash
$ nslookup newsgac.yourdomain
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	newsgac.yourdomain
Address: xxx.xxx.xxx.xxx
```

Configure outside proxy to handle SSL for this domain

Create `web-ingress.yml` for external ingress

```bash
kubectl apply -f database-claim0-persistentvolumeclaim.yaml 
kubectl apply -f newsgac-claim0-persistentvolumeclaim.yaml 
```

Manually copy contents of `platform/newsgac` to `newsgac-claim0`

```bash
kubectl apply -f web-ingress.yaml
kubectl apply -f frog-service.yaml 
kubectl apply -f redis-service.yaml 
kubectl apply -f web-service.yaml 
kubectl apply -f database-service.yaml
kubectl apply -f deployments/
```

Wait 5 minutes for containers to be created

Go to https://newsgac.yourdomain
