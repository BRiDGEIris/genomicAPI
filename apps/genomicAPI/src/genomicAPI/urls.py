#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('genomicAPI',
  url(r'^$', 'views.index'),
  
  url(r'^init/$', 'views.init'),
  
  url(r'^api_get/variants/(?P<variant_id>[a-zA-Z0-9_-]*)/$', 'views.api_get_variants'),
  url(r'^api_search/variants/$', 'views.api_search_variants'),
  url(r'^api_import/variants/$', 'views.api_import_variants'),
  url(r'^api_search/sample_id/(?P<sample_id>[a-zA-Z0-9_-]*)/$', 'views.api_search_sample_id'),
  
  url(r'^query/$', 'views.query'),
  url(r'^query_insert/$', 'views.query_insert'),
  url(r'^api/insert/general/$', 'views.api_insert_general'),
  url(r'^job/$', 'views.job'),
  url(r'^history/$', 'views.history'),
  
  url(r'^documentation/$', 'views.documentation'),
)
