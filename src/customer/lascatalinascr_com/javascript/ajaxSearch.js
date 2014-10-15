function refresh_ListingSummaryContent(data){
    // get data from the ajax request and update the Plone content
    foo = $(data).filter('#AjaxFilter');
    if( $(foo).length<1){
        //Server Error?
        foo = '<h2>Ups, something went wrong ... </h2><h3>We are sorry for the troubles. Please try find your property later again.</h3>';
    }

    $('section.listing-summary, .template-listing-detail .listing.detail').replaceWith(foo);      
    $('section.listing-summary .js-off').hide();
    $('section.listing-summary .js-on.show').show();
    $('section.listing-summary .js-on.hide').hide();
    //update listing links with search params
    linkMyParams($('.listingLink'));
    linkMyParams($('#portal-breadcrumbs a').last());
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
function refresh_Content(data, isListingSummary){
    isListingSummary = isListingSummary || false;

    if(isListingSummary){
        foo = $(data).find('section.listing-summary');

        $('section.listing-summary').replaceWith(foo);      
        $('section.listing-summary .js-off').hide();
        $('section.listing-summary .js-on.show').show();
        $('section.listing-summary .js-on.hide').hide();
    }
    else{
        foo = $(data).find('#content');
        $('#content-core').replaceWith(foo); 

    }
    
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

function ajaxLink(target, loadListingSummary, isListingSummary){
    loadListingSummary = loadListingSummary || false;
    isListingSummary = isListingSummary || false;
    //rewrite the batch to work with ajax
    $.ajax({
        url : target,
        crossDomain: true,
        success:function(data, textStatus, jqXHR){
            //data: return data from server
            if(loadListingSummary){
                refresh_ListingSummaryContent(data);
            }
            else{
                    refresh_Content(data, isListingSummary);
            }
            
        },
        error: function(jqXHR, textStatus, errorThrown){
            //if fails   
            console.log(errorThrown);   
        }
    });

}

function linkMyParams(link_obj){
    /* preserve the current filter status is a link
       serialize the form
       update the href(s) of the given link object(s)
    */
    var MyParams = "LCMARKER=1&" + $(".aJaXFilter form").serialize();
    
    $(link_obj).each(function( index ) {
        MyUrl = $(this).attr('href');  
        
        if (MyUrl.indexOf("?") > 0){
            connector ="&";
        }
        else{
            connector ="?";
        } 
     
        if(MyUrl.indexOf("LCMARKER=1") < 1){
            //our params are not set yet
            newUrl = MyUrl + connector + MyParams;
        }
        else{
            //we set this params before and have to replace them
            splitUrl= MyUrl.split('LCMARKER=1&');
            newUrl = splitUrl[0] + MyParams;
        }
        //finally: update Link Url
        $(this).attr('href', newUrl);

        
    });
}

$(document).ready(function() {
    //if the AjaxFilter Portlet is available
    // execute the AjaxSearch
    if($('.aJaXFilter').length>0){

        $(".aJaXFilter form").submit(function(e){
            e.preventDefault(); //STOP default action

            var formURL = $(this).attr("action");
            
            if($('.template-listing-detail').length<1){
                //if we are not on listing details
                // send ajax request
                var postData = $(this).serializeArray();
                
                $.ajax({
                    url : formURL,
                    type: "POST",
                    crossDomain: false,
                    data : postData,
                    success:function(data, textStatus, jqXHR){
                        //data: return data from server
                        refresh_ListingSummaryContent(data);

                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        //if fails   
                        console.log('Error:');
                        console.log(errorThrown);   
                    }
                });

            }
            else{
                splitUrl = formURL.split('@@');
                newUrl   = splitUrl[0] + "?LCMARKER=1&" + $(this).serialize();
                window.location.href = newUrl;
            }
            
        });

        //add change event to form fields
        // no submit button needed
        $(".aJaXFilter input").change(function(){
            $(".aJaXFilter form").submit();
        });

        //unset default Plone classes
        $('.aJaXFilter form').removeClass();

        //submit searchform to show results of preserved search?

        if($('section.listing-summary').length>0 && window.location.href.indexOf("LCMARKER=1") > 0){
          $(".aJaXFilter form").submit();
        }
        
        //"remember" form status in links
        linkMyParams($('.listingLink'));
        linkMyParams($('#portal-breadcrumbs a').last());
        
    }
});
