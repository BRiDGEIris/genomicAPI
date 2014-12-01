IMPORTANT: current code is for test purpose and it is far from perfect.

##**Requirements**

Library to install for python: pycurl 
Data uploaded should be added to user/hdfs/data/. Subfolders are not taken into account yet.
Data compressed will be uploaded to user/hdfs/compressed_data/. 
Those folders should be manually created by the developer if they do not exist yet.

Change the privileges for the application does not work, do it for hue in general (dumb way to do it, but it works):
```bash
cd /usr/lib/
sudo find hue -type d -exec chmod 0777 {} \;
sudo find hue -type f -exec chmod 0777 {} \;
```

##**API**

###*Authentification:*
    ```bash
    curl --data "username=cloudera&password=cloudera" -c "cookies.txt" -b "cookies.txt"
    -X POST http://quickstart.cloudera:8888/accounts/login/
    ```
###*Request:*
 * Search for files containing the <CUSTOMER_SAMPLE_ID> and return [[customer_file_id, hdfs_file_path], ...]
    (note for the developers: the customer_sample_id in db is a little bit different than this one)
    ```bash    
    curl -c "cookies.txt" -b "cookies.txt" -X GET 
    http://quickstart.cloudera:8888/genomicAPI/api/files/search/<CUSTOMER_SAMPLE_ID>/
    ```


