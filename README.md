
---


# 🚀 AOSP Logs Processor – GCP Cloud Run Deployment

This project deploys an **AOSP logs processor** service using **Google Cloud Run** and **Docker**.

---

## 🧰 Setup: Define Environment Variables

Before you begin, define the necessary variables to reuse them in all commands:

```bash
# 🔧 Basic configuration
PROJECT_ID=test_gcp_project
SERVICE_ACCOUNT_NAME=aosp-logs
REGION=us-central1
IMAGE_NAME=aosp-logs
REPO_URL=europe-docker.pkg.dev/$PROJECT_ID/aosp-logs/$IMAGE_NAME
SERVICE_ACCOUNT_EMAIL=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
CLOUD_RUN_URL=https://aosp-logs-674040060205.$REGION.run.app
````

---

## 📋 Prerequisites

Authenticate with Google Cloud and set your project:

```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```

---

## 🛠️ Create Service Account

Create a service account to be used by Cloud Run with Vertex AI access:

```bash
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --project=$PROJECT_ID \
  --description="Cloud Run SA with Vertex AI access" \
  --display-name="Cloud Run VertexAI SA"
```

---

## 🐳 Build & Push Docker Image

### 🔧 Build the image

```bash
docker build . -t $REPO_URL:latest
```

### 📤 Push the image

```bash
docker push $REPO_URL
```

---

## ☁️ Deploy to Cloud Run

Deploy your container to Cloud Run:

```bash
gcloud run deploy $IMAGE_NAME \
  --image $REPO_URL \
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID \
  --platform managed \
  --region $REGION \
  --service-account=$SERVICE_ACCOUNT_EMAIL \
  --allow-unauthenticated
```

---

## 🧪 Test the Deployment

To test your deployed service, pass a `.error` file encoded as base64:

```bash
TOKEN=$(gcloud auth print-identity-token)
MOOD="rude"

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"file_base64\": \"$(base64 -w 0 ./errors/test.aosp.txt)\", \"mood\": \"$MOOD\"}"
  $CLOUD_RUN_URL/
```

✅ If everything works, you’ll receive a response from the service.

---

## 🧾 Notes

* Ensure your service account has the following roles:

  * `Vertex AI User`
  * `Cloud Run Invoker`
  * `Cloud Run Admin`
* Modify regions and image names if your setup differs.
* For production deployments, enable authentication and secure access.

---

