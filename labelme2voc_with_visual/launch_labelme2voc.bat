echo on
call activate mkdoc
python -m labelme2voc data_annotated data_dataset_voc --labels labels.txt
pause
