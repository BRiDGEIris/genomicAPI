$(document).ready(function() {
  $("#insertForm").submit(function(e){
    e.preventDefault(e);
    
    var import_file = document.getElementById("import_file").value;
    var file_id = document.getElementById("file_id").value;
    var samples_ids = document.getElementById("samples_ids").value;
     
    var params = 'import_file='+encodeURI(import_file)+ '&file_id='+encodeURI(file_id)+'&samples_ids='+encodeURI(samples_ids);
    if (import_file == '' || file_id == '' || samples_ids == '') {
      $("#result").text('Please, fill all the fields');
      $("#result").removeClass("bad-info");
      $("#result").removeClass("great-info");
      $("#result").addClass("bad-info");
    } else {
      var $form = $("#insertForm"), url = $form.attr( "action" );
     
     //Disabling the form
     $('#insertFormSubmit').attr('disabled', 'disabled');
     $('#import_file').attr('disabled', 'disabled');
     $('#samples_ids').attr('disabled', 'disabled');
     $('#file_id').attr('disabled', 'disabled');
     
     //Say to the user to wait
      $("#result").text("Please wait...");
      $("#result").removeClass("bad-info");
      $("#result").removeClass("great-info");
      $("#result").addClass("great-info");
     
     //Sending the request
     $.ajax({
            type: 'POST',
            url: '/genomicAPI/api/general/insert/?user.name=cloudera',
            data: params,        
            dataType: 'html',
            contentType: "application/json",    
            success: function(response) {
              obj = $.parseJSON(response);
              res = obj.traceback.toSource().split("result['data'] ="); 
              var content = res.pop();
              content = content.split("'\"");
              content = content[0].split("'");
              
              if(content.length >= 2) {
                $("#result").text(String(content[1]));
                $("#result").removeClass("bad-info");
                $("#result").removeClass("great-info");
                $("#result").addClass("great-info");
              } else {
                $("#result").text("Sorry, an error occurred.");
                $("#result").removeClass("bad-info");
                $("#result").removeClass("great-info");
                $("#result").addClass("bad-info");   
              }
            }, 
            complete: function(jqXHR) {
              //Values of the form to zero
             $('#file_id').val('');
             $('#samples_ids').val('');
              
             //Enabling the form again the form
             $('#insertFormSubmit').removeAttr('disabled');
             $('#import_file').removeAttr('disabled');
             $('#samples_ids').removeAttr('disabled');
             $('#file_id').removeAttr('disabled');
            },
            error: function(jqXHR) {
              $("#result").text("Sorry, an error occurred.");
              $("#result").removeClass("bad-info");
              $("#result").removeClass("great-info");
              $("#result").addClass("bad-info");      
            } 
        });        
    }
    return false;
  });
});
