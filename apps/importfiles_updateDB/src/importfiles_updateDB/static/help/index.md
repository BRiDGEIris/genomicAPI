The Genomic File Import application lets you import your FASTQ, BAM and VCF files to the centralized system. 
Actually the files themselves should be first uploaded into your home HDFS directory. 
The user selects files from the list of available files (must be .fastq, .bam or .vcf files) and submit. The files are then archived into a centralized directory. Note that the path to the centralized directory is stored in the clinical/phenomic database. In addition, the VCF files are automatically converted to an AVRO format and also stored into the centralized directory. In addition the generated AVRO files are uploaded into HBase. All these processes are done transparently to the user such that he does not have to care about it. 

Note that the directory tree in the centralized system is the following: 

     /user/center/data
     +-- RAW/ 
     |	 |--- 380938_20141110.vcf.gz
     |   |--- 280929_20141112.vcf.gz 
     |   |--- 282802_20141110.bam 
     |	 |--- 092299_20141112.bam
     |	 |--- 280298_20141110.fastq.gz
     |	 |--- 280282_20141112.fastq.gz
     +-- AVRO/
      	 |--- 380938_20141110.avro
      	 |--- 280929_20141112.avro


The user will see in his home directory the imported files 
```/user/<username>/data/myvcfname.vcf```. The user gets full read/write access on his home folder. The ```/user/center/data``` directory is not readable/writeable by the user. It is meant to be used when the user required some data. 

A disk usage quota is assigned to each user such that the user cannot put as many files as he wants in his home directory. A new file will not be accepted if his disk usage quota is exceeded. 


The file processing workflow is the following: 

  1. Upload of the genomic file to the home directory (hdfs/data/)
  2. Storing the file in the centralized system
    * (TODO) Use ajax to submit the form
    * Assignation of a random ID for the file (6 random digits + '_' + date in '20141110' format)
    * Sequential compression of the file read from the hdfs with the output file on the local file system
    * Copy of the file into /hdfs/compressed_data/ with the generated random id
    * Insert data information in the clinical/genomic database (sample_id, file_id, fileformat)
  3. (TODO) If step is not correctly terminated (insertion in database), an error message pops up in the interface and all the files in ```/user/center/data``` and ```/user/<username>/data``` are permanently deleted .
      
