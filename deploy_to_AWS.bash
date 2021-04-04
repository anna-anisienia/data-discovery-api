docker build -t dda .
aws ecr create-repository --repository-name dda
docker tag dda:latest 123456789.dkr.ecr.eu-central-1.amazonaws.com/dda:latest
aws ecr get-login-password | docker login --username AWS --password-stdin 123456789.dkr.ecr.eu-central-1.amazonaws.com
docker push 123456789.dkr.ecr.eu-central-1.amazonaws.com/dda:latest
