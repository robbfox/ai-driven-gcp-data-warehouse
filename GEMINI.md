# Gemini Session Commands

## Command 1: Check gcloud CLI installation
```bash
gcloud --version
```

## Command 2: Create GCP Storage Bucket
```bash
gcloud storage buckets create gs://robb-gemini-bq --project=robbproject1 --location=US-CENTRAL1
```

## Command 3: Upload files to GCP Storage Bucket
```bash
gcloud storage cp C:/Users/robbf/Documents/ai-driven-gcp-data-warehouse/archive/<filename> gs://robb-gemini-bq/
```
(Repeat for each file in the 'archive' directory)