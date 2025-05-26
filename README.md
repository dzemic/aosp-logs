🚀 AOSP Logs Processor – GCP Cloud Run Deployment
This project deploys an AOSP logs processor service using Google Cloud Run and Docker.

📋 Prerequisites
Before starting, authenticate with Google Cloud and select your project:

bash
Copy
Edit
gcloud auth login
gcloud config set project vw-cariad-ivicariad-ivi-ci-dzv
🛠️ Create Service Account
Create a service account to be used by Cloud Run with Vertex AI access:

bash
Copy
Edit
SERVICE_ACCOUNT_NAME=aosp-logs
PROJECT_ID=vw-cariad-ivicariad-ivi-ci-dzv

gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --project=$PROJECT_ID \
  --description="Cloud Run SA with Vertex AI access" \
  --display-name="Cloud Run VertexAI SA"
🐳 Build & Push Docker Image
🔧 Build the image
bash
Copy
Edit
docker build . -t europe-docker.pkg.dev/vw-cariad-ivicariad-ivi-ci-dzv/aosp-logs/aosp-logs:latest
📤 Push the image
bash
Copy
Edit
docker push europe-docker.pkg.dev/vw-cariad-ivicariad-ivi-ci-dzv/aosp-logs/aosp-logs
☁️ Deploy to Cloud Run
Deploy your container to Cloud Run with the required configuration:

bash
Copy
Edit
gcloud run deploy aosp-logs \
  --image europe-docker.pkg.dev/vw-cariad-ivicariad-ivi-ci-dzv/aosp-logs/aosp-logs \
  --set-env-vars GCP_PROJECT_ID=vw-cariad-ivicariad-ivi-ci-dzv \
  --platform managed \
  --region us-central1 \
  --service-account="aosp-logs@vw-cariad-ivicariad-ivi-ci-dzv.iam.gserviceaccount.com" \
  --allow-unauthenticated
🧪 Test the Deployment
To test your deployment, pass an .error file encoded as base64:

bash
Copy
Edit
TOKEN=$(gcloud auth print-identity-token)

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"file_base64\": \"$(base64 -w 0 ./errors/test.aosp.txt)\"}" \
  https://aosp-logs-674040060205.us-central1.run.app/
✅ If everything works, you’ll receive a response from the service.

🧾 Notes
Ensure your service account has sufficient IAM permissions:

Vertex AI User

Cloud Run Invoker

Cloud Run Admin

And any other required roles

Update the region or project name if your setup differs.

For production deployments, consider enabling authentication and securing your endpoints.
