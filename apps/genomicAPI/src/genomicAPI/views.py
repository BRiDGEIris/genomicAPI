#!/usr/bin/env python

from desktop.lib.django_util import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from genomicAPI.forms import *
import pycurl
from StringIO import StringIO
from random import randrange
import bz2
import os.path

import logging
import json
from desktop.context_processors import get_app_name
from desktop.lib.django_util import render
from django.http import HttpResponse
import time
import datetime
from beeswax.design import hql_query
from beeswax.server import dbms
from beeswax.server.dbms import get_query_server_config
from impala.models import Dashboard, Controller

""" ************** """
""" USER INTERFACE """
""" ************** """

def index(request):
  return render('index.mako', request, locals())

def job(request):
  return render('job.mako', request, locals())

@csrf_exempt
def query(request):
  if request.method == 'POST':
    form = query_form(request.POST)  
  else:
    form = query_form()
  return render('query.mako', request, locals())

@csrf_exempt
def query_insert(request):
  #we list the different file in the current directory
  info = get_cron_information("http://localhost:14000/webhdfs/v1/user/hdfs/data/?op=LISTSTATUS")
  files = json.loads(info)
  filesList = {}
  for f in files[u"FileStatuses"][u"FileStatus"]:
    if f[u"pathSuffix"].endswith(".vcf") or f[u"pathSuffix"].endswith(".bam") or f[u"pathSuffix"].endswith(".fastq") or f[u"pathSuffix"].endswith(".fq"):
      filesList[f[u"pathSuffix"]] = "data/"+f[u"pathSuffix"]
  
  return render('query_insert.mako', request, locals())
  
  
  
def init(request):  
  #connexion to the db
  query_server = get_query_server_config(name='impala')
  db = dbms.get(request.user, query_server=query_server)
  
  #The sql queries
  sql = '''DROP TABLE IF EXISTS map_sample_id; CREATE TABLE map_sample_id (internal_sample_id STRING, customer_sample_id STRING, date_creation TIMESTAMP, date_modification TIMESTAMP);  DROP TABLE IF EXISTS sample_files; CREATE TABLE sample_files (id STRING, internal_sample_id STRING, file_path STRING, file_type STRING, date_creation TIMESTAMP, date_modification TIMESTAMP);'''
  #DROP TABLE IF EXISTS variants; CREATE TABLE variants (id STRING, alternate_bases STRING, calls STRING, names STRING, info STRING, reference_bases STRING, quality DOUBLE, created TIMESTAMP, elem_start BIGINT, elem_end BIGINT, variantset_id STRING); DROP TABLE IF EXISTS variantsets; 
  #CREATE TABLE variantsets (id STRING, dataset_id STRING, metadata STRING, reference_bounds STRING);
  #DROP TABLE IF EXISTS datasets; CREATE TABLE datasets (id STRING, is_public BOOLEAN, name STRING);'''
  
  #Executing the different queries
  tmp = sql.split(';')
  for hql in tmp:
    hql = hql.strip()
    if hql:
      query = hql_query(hql)
      handle = db.execute_and_wait(query, timeout_sec=5.0)
     
  return render('init.mako', request, locals())
  
def init_example(request):
  result = {
    'status': -1,
    'data': {}
  }
  query_server = get_query_server_config(name='impala')
  db = dbms.get(request.user, query_server=query_server)
  
  #Deleting the db
  hql = "DROP TABLE IF EXISTS val_test_2;" 
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  
  #Creating the db
  hql = "CREATE TABLE val_test_2 (id int, token string);" 
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  
  #Adding some data  
  hql = " INSERT OVERWRITE val_test_2 values (1, 'a'), (2, 'b'), (-1,'xyzzy');" 
  #hql = "INSERT INTO TABLE testset_bis VALUES (2, 25.0)" 
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  
  #querying the data
  hql = "SELECT * FROM val_test_2"
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  if handle:
    data = db.fetch(handle, rows=100)
    result['data'] = list(data.rows())
    db.close(handle)
 
  return render('init.mako', request, locals())
  
def history(request):
  return render('history.mako', request, locals())
  
def documentation(request):
  return render('documentation.mako', request, locals())

""" *** """
""" API """
""" *** """

def api_get_variants(request, variant_id):
  result = {
    'status': -1,
    'data': {}
  }
  
  #Connexion db
  query_server = get_query_server_config(name='impala')
  db = dbms.get(request.user, query_server=query_server)
    
  #Selecting the information related to the variant
  hql = "SELECT * FROM map_sample_id;"
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  if handle:
    data = db.fetch(handle, rows=100)
    result['data'] = list(data.rows())
    result['status'] = 1
    db.close(handle)

  #Returning the data
  return HttpResponse(json.dumps(result), mimetype="application/json")
  
def api_search_variants(request):
  result = {
    'status': -1,
    'data': {}
  }
  
  #Returning the data
  return HttpResponse(json.dumps(result), mimetype="application/json")
  
def api_import_variants(request):
  result = {
    'status': -1,
    'data': {}
  }
  
  #Returning the data
  return HttpResponse(json.dumps(result), mimetype="application/json")
  
  
def api_search_sample_id(request, sample_id):
  sample_id = str(sample_id)
  result = {
    'status': -1,
    'data': {}
  }
  
  #Connexion db
  query_server = get_query_server_config(name='impala')
  db = dbms.get(request.user, query_server=query_server)
  customer_sample_id = str(request.user.id)+"_"+sample_id  
    
  #Selecting the files related to the sample id
  hql = "SELECT sample_files.id, sample_files.file_path FROM sample_files JOIN map_sample_id ON sample_files.internal_sample_id = map_sample_id.internal_sample_id WHERE map_sample_id.customer_sample_id = '"+customer_sample_id+"';"
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  if handle:
    data = db.fetch(handle, rows=100)
    result['data'] = list(data.rows())
    result['status'] = 1
    db.close(handle)

  #Returning the data
  return HttpResponse(json.dumps(result), mimetype="application/json")
  
def api_insert_general(request):
  #we list the different file in the current directory
  info = get_cron_information("http://localhost:14000/webhdfs/v1/user/hdfs/data/?op=LISTSTATUS")
  files = json.loads(info)
  filesList = {}
  for f in files[u"FileStatuses"][u"FileStatus"]:
    if f[u"pathSuffix"].endswith(".vcf") or f[u"pathSuffix"].endswith(".bam") or f[u"pathSuffix"].endswith(".fastq") or f[u"pathSuffix"].endswith(".fq"):
      filesList[f[u"pathSuffix"]] = "data/"+f[u"pathSuffix"]
  
  result = {
    'status': -1,
    'data': 'Invalid data sent.'
  }
  
  #We check if we have received some data to import
  formValidated = False
  if request.method == 'POST':
    form = query_insert_form(request.POST, files=filesList)
    if form.is_valid():
      file_id = form.cleaned_data['file_id']
      samples_ids = form.cleaned_data['samples_ids']
      selected_file = form.cleaned_data['import_file']
      
      if selected_file.endswith(".vcf"):
        file_type = "vcf"
      elif selected_file.endswith(".bam"):
        file_type = "bam"
      elif selected_file.endswith("fastq") or selected_file.endswith("fq"):
        file_type = "fastq"
      else:
        file_type = "unknown"
      
      #Generating the random id for the file
      file_random_id = create_random_file_id()
      
      #Compressing the file and writing it directly in the correct directory
      path = "data/"+selected_file.strip()
      destination = file_random_id+".bz2"
      result = compress_file(path, destination)
      
      #Connexion to the db
      query_server = get_query_server_config(name='impala')
      db = dbms.get(request.user, query_server=query_server)
      dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     
      #We insert the data to the db
      #TODO: Not very optimized if we have 100 samples ids to insert...
      tmp = samples_ids.split('\n')
      for current_id in tmp:
        current_id = current_id.strip()
        if len(current_id) > 0:
          
          customer_sample_id = str(request.user.id)+"_"+current_id
          internal_sample_id = ""
          
          #We check if we already have an internal_sample_id for the customer_sample_id given
          query = hql_query("SELECT internal_sample_id FROM map_sample_id WHERE customer_sample_id = '"+customer_sample_id+"' LIMIT 1;")
          handle = db.execute_and_wait(query, timeout_sec=5.0)
          
          if handle:
            #If yes, we take the same as before.
            data = db.fetch(handle, rows=1)
            tmp = list(data.rows())
            if(len(tmp) > 0):
              internal_sample_id = tmp.pop().pop()
          
          if len(internal_sample_id) == 0:
            #If not, we create a new customer_sample_id and save it 
            internal_sample_id = str(request.user.id)+"_"+create_random_sample_id()
            
            query = hql_query("INSERT INTO map_sample_id VALUES('"+internal_sample_id+"', '"+customer_sample_id+"', '"+dt+"', '"+dt+"');")
            handle = db.execute_and_wait(query, timeout_sec=5.0)
        
          #We can insert the data now.
          query = hql_query("INSERT INTO TABLE sample_files VALUES ('"+file_id+"', '"+internal_sample_id+"', '"+destination+"', '"+file_type+"', '"+dt+"', '"+dt+"')")
          handle = db.execute_and_wait(query, timeout_sec=5.0)
     
      #End
      result['data'] = 'Data correctly added.'
      
  #Returning the data
  return HttpResponse(json.dumps(result), mimetype="application/json")
  
""" ************** """
""" SOME FUNCTIONS """
""" ************** """
  
def get_cron_information(url, post_parameters=False):
  buff = StringIO()
  #Adding some parameters to the url
  if "?" in url:
    url += "&user.name=cloudera"
  else:
    url += "?user.name=cloudera"
  fprint("Access to: "+url)
  
  c = pycurl.Curl()
  c.setopt(pycurl.URL, str(url))
  c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
  c.setopt(c.WRITEFUNCTION, buff.write)
  #c.setopt(pycurl.VERBOSE, 0)
  c.setopt(pycurl.USERPWD, 'cloudera:cloudera')
  if post_parameters:
    c.setopt(c.POST, 1)
    c.setopt(c.HTTPPOST, post_parameters)
  c.perform()
  c.close()
  return buff.getvalue()

def upload_cron_information(url, filename):
  fout = StringIO()
  
  #Adding some parameters to the url
  if "?" in url:
    url += "&user.name=cloudera"
  else:
    url += "?user.name=cloudera"
  fprint(url)
  
  #Setting the headers to say that we are uploading a file. See http://www.saltycrane.com/blog/2012/08/example-posting-binary-data-using-pycurl/
  c = pycurl.Curl()
  c.setopt(pycurl.VERBOSE, 1)  
  c.setopt(pycurl.WRITEFUNCTION, fout.write)
  c.setopt(pycurl.URL, str(url))
  c.setopt(pycurl.UPLOAD, 1)
  c.setopt(pycurl.READFUNCTION, open(filename, 'rb').read)
  c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/octet-stream'])
  filesize = os.path.getsize(filename)
  c.setopt(pycurl.INFILESIZE, filesize)
  c.perform()
  
  fprint(c.getinfo(pycurl.RESPONSE_CODE))
  fprint(fout.getvalue())
  print fout.getvalue()

def create_random_sample_id():
  now = datetime.datetime.now()
  y = now.year
  m = now.month
  d = now.day
  h = now.hour
  minute = now.minute
  if len(str(m)) == 1:
    m = "0"+str(m)
  if len(str(d)) == 1:
    d = "0"+str(d)
  if len(str(h)) == 1:
    h = "0"+str(h)
  if len(str(minute)) == 1:
    minute = "0"+str(minute)
  
  randomId = str(randrange(100000,999999))
  randomId += "_"+str(y)+str(m)+str(d)+str(h)+str(minute)
  return randomId
  
def create_random_file_id():
  now = datetime.datetime.now()
  y = now.year
  m = now.month
  d = now.day
  if len(str(m)) == 1:
    m = "0"+str(m)
  if len(str(d)) == 1:
    d = "0"+str(d)
  
  randomId = str(randrange(100000,999999))
  randomId += "_"+str(y)+str(m)+str(d)
  return randomId
  
def copy_file(origine, destination):
  return True
  
def compress_file(path, destination):
  data = ""
  
  #Open a temporary file on the local file system (not a big deal) for the compression. It will be deleted after
  temporary_filename = "tmp."+str(randrange(0,100000))+".txt"
  f = open(temporary_filename,'w')
  content = "Coucou, comment, ca va?"
  content_splitted = content.split(',')
  
  #creating a compressor object for sequential compressing
  comp = bz2.BZ2Compressor()
  
  #We take the length of the file to compress
  file_status = get_cron_information("http://localhost:14000/webhdfs/v1/user/hdfs/"+path+"?op=GETFILESTATUS")
  file_status = json.loads(file_status)
  file_length = file_status[u"FileStatus"][u"length"]
  
  #We take part of the file to compress it
  offset=0
  while offset < file_length:
    length = min(file_length,1024*1024)
    txt = get_cron_information("http://localhost:14000/webhdfs/v1/user/hdfs/"+path+"?op=OPEN&offset="+str(offset)+"&length="+str(length)+"")
    data += comp.compress(txt)
    fprint(txt)    
    
    #If we have already compressed some data we write them
    if len(data) > 10*1024*1024:
      f.write(data)
      data = ""
    
    offset += min(length,1024*1024) #1Mo
   
  #Flushing the result
  data += comp.flush()
  f.write(data)
  f.close()
    
  #Saving the file to the new repository: http://hadoop.apache.org/docs/r1.0.4/webhdfs.html#APPEND
  result = upload_cron_information("http://localhost:14000/webhdfs/v1/user/hdfs/compressed_data/"+destination+"?op=CREATE&overwrite=false&data=true", temporary_filename)
    
  return result

def fprint(txt):
  f = open('debug.txt', 'a')
  f.write(str(txt)+"\n")
  f.close()
  return True
