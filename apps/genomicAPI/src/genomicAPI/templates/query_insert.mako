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
    <h2 class="card-heading simple">Insert/Upload Data</h2>
    <div class="card-body genomicAPI">
      % if formValidated:
        <br/>Data correctly added.<br/><br/>
      % endif
      <form action="" method="POST" class="insertForm">
        <div class="left-box">
          <label for="import_file">File to import: </label>
        </div>
        <div class="right-box">
          <select name="import_file">
            % for key, value in enumerate(filesList):
              <option value="${value}" selected>${value}</option>
            % endfor
          </select>
        </div>
        <br/>
        <div class="left-box">
          <label for="file_id">File id: </label>
        </div>
        <div class="right-box">
          <input type="text" name="file_id" id="file_id" maxlength="255" />
        </div>
        <br/>
        <div class="left-box">
          <label for="samples_ids">Samples ids (separated by a comma): </label>
        </div>
        <div class="right-box">
          <input type="text" name="samples_ids" id="samples_ids" maxlength="30000" />
        </div>
        <br/>
                        
        <input type="submit" value="Import" />
        <br/>       
      </form>
    
    </div>
  </div>
</div>
${commonfooter(messages) | n,unicode}
