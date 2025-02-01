# Use the gcloud CLI to create a GCL Cloud SQL database INSTANCE
gcloud sql instances create synthea-demo \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --root-password=de08NT22244