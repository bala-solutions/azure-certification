This windows batch script

set templateFile=C:\<userpath>\azuredeploy.json
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (set today=%%a-%%b-%%c)
set DeploymentName=blanktemplate-%today%

az deployment group create --name testdeployment1  --template-file %templateFile% --resource-group <<resource-group-id>> --parameters storageSKU=Standard_GRS storageName=balanewstoragename

