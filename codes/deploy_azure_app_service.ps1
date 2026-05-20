# Azure App Service deployment script for LangGraph-AzureAI-Agents.
# Run from repository root. Edit placeholders before using.

Set-Location (Split-Path -Parent $PSScriptRoot)

$PY = "$env:USERPROFILE\anaconda3\envs\LangAzure\python.exe"
$AZ = "C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"

$RG = "<YOUR_RESOURCE_GROUP>"
$WEBAPP = "<YOUR_APP_SERVICE_NAME>"

& $AZ account show --output table

$HOSTS = & $AZ webapp show `
  --resource-group $RG `
  --name $WEBAPP `
  --query "enabledHostNames" `
  --output tsv

$APP_HOST = ($HOSTS | Where-Object { $_ -notmatch "\.scm\." } | Select-Object -First 1)
$APP_URL = "https://$APP_HOST"

Write-Host "APP_URL = $APP_URL"

& $AZ webapp config appsettings set `
  --resource-group $RG `
  --name $WEBAPP `
  --settings `
  SCM_DO_BUILD_DURING_DEPLOYMENT="false" `
  ENABLE_ORYX_BUILD="false" `
  ENVIRONMENT="azure" `
  USE_AZURE_OPENAI_TRIAGE="true" `
  USE_AZURE_OPENAI_RESPONSE="true" `
  USE_AZURE_CONTENT_SAFETY="true" `
  PORT="8000" `
  WEBSITES_PORT="8000" `
  WEBSITES_CONTAINER_START_TIME_LIMIT="1800" `
  PYTHONUNBUFFERED="1"

& $PY codes/scripts/build_posix_zip.py

& $AZ webapp config set `
  --resource-group $RG `
  --name $WEBAPP `
  --startup-file "python -m http.server 8000 --directory /home/site/wwwroot"

& $AZ webapp start `
  --resource-group $RG `
  --name $WEBAPP

Start-Sleep -Seconds 30

& $AZ webapp deployment source config-zip `
  --resource-group $RG `
  --name $WEBAPP `
  --src deploy_app_posix.zip `
  --timeout 600

Invoke-WebRequest "$APP_URL/startup.py" -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest "$APP_URL/clinical_agent/api.py" -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest "$APP_URL/src/clinical_agent/agent/graph.py" -UseBasicParsing | Select-Object StatusCode
Invoke-WebRequest "$APP_URL/data/processed/appointment_history.csv" -UseBasicParsing | Select-Object StatusCode

& $AZ webapp config set `
  --resource-group $RG `
  --name $WEBAPP `
  --startup-file "python /home/site/wwwroot/startup.py"

& $AZ webapp restart `
  --resource-group $RG `
  --name $WEBAPP

Write-Host "First startup may take several minutes while dependencies install."
Write-Host "Swagger docs: $APP_URL/docs"
