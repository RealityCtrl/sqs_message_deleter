Compress-Archive -Path C:\Users\david\git\polling_lambda\hello_world -DestinationPath C:\tmp\code.zip
Import-Module AWSPowerShell
Write-S3Object -BucketName lambda-deployment-realityctrl-sndbx -File C:\tmp\poller_code.zip
$content = [IO.File]::ReadAllText("C:\Users\david\git\polling_lambda\template.yaml")
$JSONFile = ConvertFrom-Json "$(get-content $(Join-Path C:\Users\david\git\polling_lambda\ "params.json"))"
New-CFNStack -StackName mysqshelperlayerstack -TemplateBody $content -Parameter $JSONFile