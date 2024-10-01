# Helpful commands

Find the number of files in total:

```bash
# linux
find tree_recognition/images/ -mindepth 2 -maxdepth 2 | wc -l
# windows (powershell)
Get-ChildItem -Path tree_recognition/images/ -Directory | ForEach-Object {$sum += (Get-ChildItem -Path $_.FullName | Measure-Object).Count} | Write-Host $sum
```
