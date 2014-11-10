genomicAPI
==========

genomicAPI is a set of API developed with Hue SDK for accessing genomic data stored in various databases (HBase, MySQL, etc).



Get started
===========
# download cloudera virtual box image 
http://www.cloudera.com/content/cloudera/en/documentation/DemoVMs/Cloudera-QuickStart-VM/cloudera_quickstart_vm.html

# decompressed the 7z to get a vmdk file
# click right on the file and select Extract here

# start your Cloudera image (click on New VM, choose centOS as OS, select the decompressed .vmdk you just downloaded)   

# in your Cloudera VM desktop, open a terminal 
# download hue 
git clone https://github.com/cloudera/hue.git

# install dependencies
yum install ant \
        asciidoc \
        cyrus-sasl-devel \
        cyrus-sasl-gssapi \
        gcc \
        gcc-c++ \
        krb5-devel \
        libtidy (for unit tests only) \
        libxml2-devel \
        libxslt-devel \
        mvn \ #(from maven package or maven3 tarball)
        mysql \
        mysql-devel \
        openldap-devel \
        python-devel \
        python-simplejson \
        sqlite-devel 
