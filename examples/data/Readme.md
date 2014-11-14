Content
=======

**patientvariablequal.csv** : CSV file with 3 columns: patientID, variantID, qual (metric to measure the quality of the variant)

Adding new table 
=================

Here are the steps to follow: 

  1. Go to the *File Browser* app
  2. Select *Upload Files* and add the csv file
  3. Go to the *Data Browser/Metastore Tables* app
  4. Click on *Create a new table from a file*
  5. Follow the steps as they appear on the screen (you can define the column names in the last step)

Here you go. You can use it directly in the Hive query text field.
To use this dataset with Impala, you need to first use the magic statement:

  ```
  INVALIDATE METADATA
  ```

which refreshes the metastore (table catalog). 

![invalidatemetadata](https://github.com/jpoullet2000/genomicAPI/blob/master/docs/images/invalidatemetadata.png)