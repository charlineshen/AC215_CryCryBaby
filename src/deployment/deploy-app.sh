echo "Testing..." >> /tmp/deploy-log.txt

ansible-playbook deploy-docker-images.yml -i inventory.yml -vvv

echo "Finishing deploy docker images"
# ansible-playbook update-k8s-cluster.yml -i inventory-prod.yml -vvv