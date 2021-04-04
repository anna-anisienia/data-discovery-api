docker build -t dda-local . -f Dockerfile.local
docker run -e AWS_ACCESS_KEY_ID=qwertzuiop -e AWS_SECRET_ACCESS_KEY=asdfghjkl -e REGION=eu-central-1 -p 8000:8000 dda-local:latest
# access the UI using: http://localhost:8000/docs