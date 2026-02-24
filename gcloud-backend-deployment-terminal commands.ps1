# Download G Cloud CLI 

# Open the powershell by default.
gcloud init

#authenticate, select project.
# Alternatively use these
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

#---------------------------------------------#
#						SETUP
#---------------------------------------------#

# Enable required services.
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com

# Check current config:
gcloud config list

# Set region - powershell
set REGION=us-central1

# gcloud terminal
gcloud config set run/region us-central1

# Create Artifact registry (Equivalent to DockerHub)
gcloud artifacts repositories create frontline-repo ^
  --repository-format=docker ^
  --location=us-central1 ^
  --description="Frontline containers"
  
# Configure Docker config
gcloud auth configure-docker us-central1-docker.pkg.dev

#Find project number (gcp) and grant permission - storage
gcloud projects add-iam-policy-binding <PROJECT_ID> ^
  --member=serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com ^
  --role=roles/storage.admin

#
gcloud projects add-iam-policy-binding <PROJECT_ID> ^
  --member=serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com ^
  --role=roles/run.admin
  
 #
 gcloud projects add-iam-policy-binding <PROJECT_ID> ^
  --member=serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com ^
  --role=roles/iam.serviceAccountUser
  
#
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/storage.admin

#
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/artifactregistry.writer

#
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
  
# cd repo-root Now build backend image.
gcloud builds submit --tag us-central1-docker.pkg.dev/<PROJECT_ID>/frontline-repo/frontline-backend:latest backend

# Create secrets/keys
```echo YOUR_GEMINI_KEY_HERE | gcloud secrets create GEMINI_API_KEY --data-file=-```
# uSE THIS instead.
- > gcloud secrets versions add GEMINI_API_KEY --data-file=<PATH_TO_SECRET_FILE>

# Do the same for each secret.

# Now check secrets = .env

gcloud secrets list

# Allow runtime access to secrets.
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor

#Deploy - paste as it is.

gcloud run deploy frontline-backend ^
  --image us-central1-docker.pkg.dev/<PROJECT_ID>/frontline-repo/frontline-backend:latest ^
  --region us-central1 ^
  --platform managed ^
  --allow-unauthenticated ^
  --set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest ^
  --set-env-vars GEMINI_MODEL=gemini-2.0-flash-lite ^
  --memory 1Gi ^
  --timeout 300
  

# get backend url
gcloud run services describe frontline-backend --region us-central1 --format="value(status.url)"



