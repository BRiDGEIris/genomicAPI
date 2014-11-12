The Genomic File Import application lets you import your FASTQ, BAM and VCF files to the centralized system. 
Actually the files themselves are copied into your home HDFS directory (keeping the same name) and into another centralized directory for archiving. Note that the path to the centralized directory is stored in the clinical/phenomic database. The VCF files are automatically converted to an AVRO format and also stored into the centralized directory. In addition the generated AVRO files are uploaded into HBase. All these processes are done transparently to the user such that he does not have to care about it. 

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

  1. Upload of the genomic file to the home directory
  2. Storing the file in the centralized system
    * Assignation of a random ID for the file (6 random digits + '_' + date in '20141110' format)
    * Copy of the file into /user/center/data 
    * Compression of the file		      
    * Renaming of the file with the just generated random ID	   
    * Insert data information in the clinical/genomic database (sampleID, fileID, fileformat)
  3. If step is not correctly terminated (insertion in database), an error message pops up in the interface and all the files in ```/user/center/data``` and ```/user/<username>/data``` are permanently deleted .
      
