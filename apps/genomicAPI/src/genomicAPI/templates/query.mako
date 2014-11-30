<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

${commonheader("Genomicapi", "genomicAPI", user) | n,unicode}
${shared.menubar(section='query')}

<link rel="stylesheet" href="/genomicAPI/static/css/genomicAPI.css">
<link rel="stylesheet" href="/genomicAPI/static/css/genomicAPI.js">

## Use double hashes for a mako template comment
## Main body

<div class="container-fluid">
  <div class="card">
    <h2 class="card-heading simple">Query your data</h2>
    <div class="card-body genomicAPI">
      <p class="info">
        See the <a href="/genomicAPI/documentation/">documentation</a> to learn the small differences between 
        the queries in SQL you are used to, and the ones you can make
        on Genomic API.<br/>
        <a href="/genomicAPI/query_insert/">Insert/Upload data</a>
      </p>
      
      <form action="" method="POST" class="queryForm">
        <br/>
        <div class="left-box">
        <label for="query_type">Type of query:</label>
        </div>
        <div class="right-box">
          <select name="query_type">
            <option value="0" selected>Genomic API (SQL-Like)</option>
            <option value="1">Google Genomics</option>
            <option value="2">HBase</option>
            <option value="3">Hive</option>
          </select><br/><br/>
        </div>
        <br/>
        <div class="left-box">
          <label for="query">Query:</label>
        </div>
        <div class="right-box">
          <textarea class="right-box" rows="5" name="query" cols="100" maxlength="500"></textarea>
          <br/><br/>
        </div>
        <br/>
        <input type="submit" value="Execute" />
        <br/>
      </form>
    
    </div>
  </div>
</div>
${commonfooter(messages) | n,unicode}
