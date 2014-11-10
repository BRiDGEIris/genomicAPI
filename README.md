genomicAPI
==========

genomicAPI is a set of API developed with Hue SDK for accessing genomic data stored in various databases (HBase, MySQL, etc).



Development: getting started with Hue SDK
=========================================
Download cloudera virtual box image:

        $ wget http://www.cloudera.com/content/cloudera/en/documentation/DemoVMs/Cloudera-QuickStart-VM/cloudera_quickstart_vm.html

Decompressed the 7z to get a vmdk file
Click right on the zipped file and select Extract here

Start your Cloudera image (click on New VM, choose centOS as OS, select the decompressed .vmdk you just downloaded) In your Cloudera VM desktop, open a terminal. 
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
