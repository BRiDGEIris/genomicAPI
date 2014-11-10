genomicAPI
==========

genomicAPI is a set of API developed with Hue SDK for accessing genomic data stored in various databases (HBase, MySQL, etc).



Development: getting started with Hue SDK
=========================================
Download cloudera virtual box image:

        $ wget http://www.cloudera.com/content/cloudera/en/documentation/DemoVMs/Cloudera-QuickStart-VM/cloudera_quickstart_vm.html

Decompressed the 7z to get a vmdk file
Click right on the zipped file and select Extract here

Start your Cloudera image (click on New VM, choose centOS as OS, select the decompressed .vmdk you just downloaded).

----

If you do not use the cloudera VM, you need to install the hue sdk 
Download hue: 

        $ git clone https://github.com/cloudera/hue.git

Install dependencies:

        $ sudo yum install ant \
                asciidoc \
                cyrus-sasl-devel \
                cyrus-sasl-gssapi \
                gcc \
                gcc-c++ \
                krb5-devel \
                libtidy \  
                libxml2-devel \
                libxslt-devel \
                mvn  \
                mysql \
                mysql-devel \
                openldap-devel \
                python-devel \
                python-simplejson \
                sqlite-devel 

With *mvn* from maven package or maven3 tarball, and 
*libtidy* for unit test only

Follow the Hue SDK tutorial from http://archive.cloudera.com/cdh/3/hue/sdk/sdk.html#from-30000-feet.
Install the Hue apps environment: 

        $ cd hue
        $ make apps
        ...
        
----

From here on, we are considering you are working on the Cloudera VM.

Open a terminal in your VM:

        $ cd sr/lib/hue
        $ mkdir myapps
        $ cd myapps
        $ sudo ./usr/lib/hue/build/env/bin/hue create_desktop_app calculator
        
If your hue directory is not the one mentioned here above, find it by:

        $ sudo whereis hue
        
Install your calculator app

        $ sudo ./../build/env/bin/python ../tools/app_reg/app_reg.py --install calculator
        
Restart the Hue service to see your changes:

        $ sudo service hue restart
        
You should be able to see another tab in your browser: *Other apps*. Click on it, you should see your *calculator* app.

![calculator app](https://github.com/jpoullet2000/genomicAPI/blob/master/docs/images/hueapp.png)
