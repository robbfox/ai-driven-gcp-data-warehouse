# In .github/workflows/your-workflow-file.yml

name: 'Deploy Infrastructure with Terraform'

on:
  push:
    branches:
      - main # Or your default branch
  pull_request:

permissions:
  contents: 'read'
  # This permission is required for Workload Identity Federation, a more advanced auth method.
  # It's good practice to include it even if you're using SA keys.
  id-token: 'write'

jobs:
  terraform:
    name: 'Terraform'
    runs-on: ubuntu-latest

    steps:
      # Step 1: Check out your repository code
      - name: Checkout
        uses: actions/checkout@v4

      # Step 2: Authenticate to Google Cloud. THIS IS THE MISSING STEP.
      # It uses the secret you created to log in.
      - name: Authenticate to Google Cloud
        id: auth
        uses: 'google-github-actions/auth@v1'
        with:
          # Make sure 'GCP_SA_KEY' EXACTLY matches the name of your GitHub secret
          credentials_json: '${{ secrets.GCP_SA_KEY }}'

      # Step 3: Set up Terraform CLI
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          # You can specify a specific version of Terraform if needed
          terraform_version: 'latest'

      # Step 4: Run Terraform Init
      # Now that the runner is authenticated, this will succeed.
      - name: Terraform Init
        id: init
        run: terraform init

      # Step 5: Run Terraform Plan
      # The -var flag is optional if the project_id is in your credentials, but explicit is better.
      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -var="project_id=your-gcp-project-id"

      # Step 6: Run Terraform Apply ONLY on pushes to the main branch
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve -no-color -var="project_id=your-gcp-project-id"