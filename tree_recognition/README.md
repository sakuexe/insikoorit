# Helpful commands

Find the number of files in total:

```bash
# linux
find tree_recognition/images/ -mindepth 2 -maxdepth 2 | wc -l
# windows (powershell)
Get-ChildItem -Path tree_recognition/images/ -Directory | ForEach-Object {$sum += (Get-ChildItem -Path $_.FullName | Measure-Object).Count} | Write-Host $sum
```

Reshuffle the tree images

```bash
# remove the image folders
rm -rf trees_training/ trees_valuation/
# get the base image folder
git checkout 047d5f0977f23ee910fe20e903eb45c8c1d78b68 -- trees_training
# run the python script
python3 organize_training.py
# commit and push your reshuffle
```
