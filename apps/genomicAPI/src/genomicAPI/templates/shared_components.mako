
<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

<%def name="menubar(section='')">
  <div class="navbar navbar-inverse navbar-fixed-top nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="currentApp">
              <a href="/genomicAPI">
                <img src="/genomicAPI/static/art/icon_genomicAPI_48.png" class="app-icon" />
                Genomicapi
              </a>
             </li>
             <li class="${is_selected(section, 'index')}"><a href="/genomicAPI/">Index</a></li>
             <li class="${is_selected(section, 'query')}"><a href="/genomicAPI/query/">Query</a></li>
             <li class="${is_selected(section, 'job')}"><a href="/genomicAPI/job/">Job</a></li>
             <li class="${is_selected(section, 'history')}"><a href="/genomicAPI/history/">History</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
