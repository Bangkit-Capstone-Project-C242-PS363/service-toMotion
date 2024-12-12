HOST=http://localhost:8080
sleep 1
curl -X POST -H "Content-Type: application/json" -d '{"data":"I want to eat"}' $HOST/tomotion | jq
