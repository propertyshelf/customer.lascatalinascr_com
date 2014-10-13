function refresh_content(data){
  // get data from the ajax request and update the Plone content
  foo = $(data).filter('#AjaxFilter');
  $('section.listing-summary').replaceWith(foo);


}

$(document).ready(function() {

    //if the AjaxFilter Portlet is available
    // execute the AjaxSearch
    if($('.aJaXFilter').length>0){

        $(".aJaXFilter form").submit(function(e){

            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");

            $.ajax({
                url : formURL,
                type: "POST",
                crossDomain: false,
                data : postData,
                success:function(data, textStatus, jqXHR){
                    //data: return data from server
                    refresh_content(data);
                },
                error: function(jqXHR, textStatus, errorThrown){
                    //if fails   
                    console.log('Error:');
                    console.log(errorThrown);   
                }
            });

            e.preventDefault(); //STOP default action
        });


    }

});
