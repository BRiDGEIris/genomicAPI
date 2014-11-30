#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import json

from desktop.context_processors import get_app_name
from desktop.lib.django_util import render
from django.http import HttpResponse

import datetime

from beeswax.design import hql_query
from beeswax.server import dbms
from beeswax.server.dbms import get_query_server_config

from impala.models import Dashboard, Controller

# def index(request):
#   return render('index.mako', request, dict(date=datetime.datetime.now()))

def index(request):
  result = {
    'status': -1,
    'data': {}
  }
  # app_name = get_app_name(request)
  # query_server = get_query_server_config(app_name)  
  query_server = get_query_server_config(name='impala')
  db = dbms.get(request.user, query_server=query_server)
    

  #hql = "SELECT * FROM testset"
  hql = "INSERT INTO TABLE testset ( patientid,variantid,qual ) VALUES ( 'patient11','variant23',29);"
  query = hql_query(hql)
  handle = db.execute_and_wait(query, timeout_sec=5.0)
  if handle:
    data = db.fetch(handle, rows=100)
    result['data'] = list(data.rows())
    db.close(handle)

  return HttpResponse(json.dumps(result), mimetype="application/json")
  
