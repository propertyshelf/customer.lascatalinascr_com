function refresh_ListingContent(data){
    // get data from the ajax request and update the Plone content
    foo = $(data).filter('#AjaxFilter');
    if( $(foo).length<1){
        //Server Error?
        foo = '<h2>Ups, something went wrong ... </h2><h3>We are sorry for the troubles. Please try find your property later again.</h3>';
    }

    $('section.listing-summary').replaceWith(foo);      
    $('section.listing-summary .js-off').hide();
    $('section.listing-summary .js-on.show').show();
    $('section.listing-summary .js-on.hide').hide();

    //refresh prepOverlay
    try{
        plonePrettyPhoto.enable(); 
    }
    catch(error){
        console.log(error);
    }
    //Pagination Links
    $("#AjaxFilter .listingBar a" ).click(function(event){
        event.preventDefault();
        myUrl = $(this).attr('href');
        ajaxLink(myUrl, true);
        return false;
    });
   

}
function refresh_Content(data){
    foo = $(data).find('section.listing-summary');

    $('section.listing-summary').replaceWith(foo);      
    $('section.listing-summary .js-off').hide();
    $('section.listing-summary .js-on.show').show();
    $('section.listing-summary .js-on.hide').hide();

    //refresh prepOverlay
    try{
        plonePrettyPhoto.enable(); 
    }
    catch(error){
        console.log(error);
    }
 

    //standard pagination links
    //not set by ajaxFilter
    if($('#AjaxFilter').length<1){
        $(".listing-summary' .listingBar a" ).click(function(event){
            event.preventDefault();
            myUrl = $(this).attr('href');
            ajaxLink(myUrl, false);
            return false;
        });
    }
}

function ajaxLink(target, isListing){
    isListing = isListing || false;
    //rewrite the batch to work with ajax
    $.ajax({
        url : target,
        crossDomain: true,
        success:function(data, textStatus, jqXHR){
            //data: return data from server
            if(isListing){
                refresh_ListingContent(data);
            }
            else{
                refresh_Content(data);
            }
            
        },
        error: function(jqXHR, textStatus, errorThrown){
            //if fails   
            console.log('Error:');
            console.log(errorThrown);   
        }
    });

}

$(document).ready(function() {
    //if the AjaxFilter Portlet is available
    // execute the AjaxSearch
    if($('.aJaXFilter').length>0){
        //unset default Plone classes
        $('.aJaXFilter form').removeClass();

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
                    refresh_ListingContent(data);

                },
                error: function(jqXHR, textStatus, errorThrown){
                    //if fails   
                    console.log('Error:');
                    console.log(errorThrown);   
                }
            });

            e.preventDefault(); //STOP default action
        });

        //add change event to form fields
        // no submit button needed
        $(".aJaXFilter input").change(function(){
            $(".aJaXFilter form").submit();
        });

        //standard pagination links
        //not set by ajaxFilter
        if($('#AjaxFilter').length<1){
            $(".listing-summary' .listingBar a" ).click(function(event){
                event.preventDefault();
                myUrl = $(this).attr('href');
                ajaxLink(myUrl, false);
                return false;
            });
        }
        

    }
});
