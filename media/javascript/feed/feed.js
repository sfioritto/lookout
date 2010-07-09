$(document).ready(
function(){


    $("select.relfilter").change(
    function(event){
	var select = $(event.target).hide();
	var text = $("select.relfilter :selected").text();
	$("a.relfilter").html(text).show();
    });

    $("a.relfilter").click(
    function(event){
	$(event.target).hide();
	$("select.relfilter").show();
	event.preventDefault();
    });

    /* go to the visit url on the hidden anchor tag instead of the href on the event target*/
    $("a.blurb, a.textbtn").click(
    function(event){
	var container = $(event.currentTarget).parents("li.blurb");
	var url = $("a.visit", container)[0].href;
	var oldurl = event.currentTarget.href;
	event.currentTarget.href = url;
	$(container).addClass("visited");
	setTimeout(function(){
		       event.currentTarget.href = oldurl;
		   }, 0);
    });

    /*mark the div as irrelevant and post to the relevance view*/
    $("a.relevance").click(
    function(event){

	var relevance = "false",
	blurb = $(event.target).parent().parent();

	if (blurb.hasClass("irrelevant")){
	    relevance = "true";
	    blurb.removeClass("irrelevant");
	} else {
	    blurb.addClass("irrelevant");
	}

	$.post(event.target.href, {
		   'relevance' : relevance
	       });
	event.preventDefault();
    });
});
