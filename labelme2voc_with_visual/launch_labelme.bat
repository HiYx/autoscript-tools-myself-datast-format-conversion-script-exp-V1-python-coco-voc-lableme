echo on
call activate mkdoc
labelme data_annotated --labels labels.txt --nodata --validatelabel exact 
pause
