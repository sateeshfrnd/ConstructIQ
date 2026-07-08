Remove-Item -Path "c:\SATISH-KUMAR\GitRepos\ConstructIQ\backend\__pycache__" -Recurse -Force
Remove-Item -Path "c:\SATISH-KUMAR\GitRepos\ConstructIQ\backend\*\__pycache__" -Recurse -Force


Get-ChildItem -Path "c:\SATISH-KUMAR\GitRepos\ConstructIQ\backend" -Recurse -Directory -Name "__pycache__" | ForEach-Object { Remove-Item "c:\SATISH-KUMAR\GitRepos\ConstructIQ\backend\$_" -Recurse -Force }