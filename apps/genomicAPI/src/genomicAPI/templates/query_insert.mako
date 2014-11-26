<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

${commonheader("Genomicapi", "genomicAPI", user) | n,unicode}
${shared.menubar(section='query')}

## Use double hashes for a mako template comment
## Main body

<div class="container-fluid">
  <div class="card">
    <h2 class="card-heading simple">Insert/Upload Data</h2>
    <div class="card-body">
      % if formValidated:
        <br/>Data correctly added.<br/><br/>
        
      % endif
      <form action="" method="POST">
        <label for="import_file">File to import: </label>
        <select name="import_file">
	        % for key, value in enumerate(filesList):
            <option value="${value}" selected>${value}</option>
	        % endfor
        </select>
        <br/>
        <label for="file_id">File id: </label>
        <input type="text" name="file_id" id="file_id" maxlength="255" />
        <br/>
        <label for="samples_ids">Samples ids (separated by a comma): </label>
        <input type="text" name="samples_ids" id="samples_ids" maxlength="30000" />
        <br/>
                        
        <input type="submit" value="Import" />
        <br/>       
      </form>
    
    </div>
  </div>
</div>
${commonfooter(messages) | n,unicode}
