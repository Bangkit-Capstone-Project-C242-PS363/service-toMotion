# build
podman build -t signmaster-tomotion .

# deploy
podman tag signmaster-tomotion asia-southeast2-docker.pkg.dev/capstone-project-c242-ps363/backend/signmaster-tomotion
podman push asia-southeast2-docker.pkg.dev/capstone-project-c242-ps363/backend/signmaster-tomotion
gcloud run deploy signmaster-tomotion --image=asia-southeast2-docker.pkg.dev/capstone-project-c242-ps363/backend/signmaster-tomotion --platform=managed --region=asia-southeast2 --allow-unauthenticated --memory=2Gi --cpu=2

# update nginx
gcloud run services describe signmaster-tomotion --platform=managed --region=asia-southeast2 --format='value(status.url)'
