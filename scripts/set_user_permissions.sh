gcloud projects add-iam-policy-binding hca-sandbox --member="user:bennie.haelen@insight.com" --role="roles/cloudsql.databases.create"
gcloud projects add-iam-policy-binding hca-sandbox --member="user:bennie.haelen@insight.com" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding hca-sandbox --member="user:bennie.haelen@insight.com" --role="roles/owner"
gcloud projects add-iam-policy-binding hca-sandbox --member="user:bennie.haelen@insight.com" --role="roles/cloudsql.client"
gcloud iam test-permissions hca-sandbox --permissions=sql.databases.create

gcloud iam roles create customCloudSqlCreator --project=hca-sandbox --title="Custom Cloud SQL Creator" --permissions="cloudsql.databases.create" --stage="GA"
gcloud projects add-iam-policy-binding hca-sandbox --member="user:bennie.haelen@insight.com" --role="projects/hca-sandbox/roles/customCloudSqlCreator"

