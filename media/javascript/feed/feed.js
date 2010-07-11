$(document).ready(
function(){

    var bind_event_handlers = function(){
	bind_select();
	bind_filter_link();
	bind_visit_link();
	bind_thumb_button();
    };

    /* Update the filter*/
    var bind_select = function(){
	$("select.relfilter").change(
	    function(event){

		var select = $(event.target).hide(),
		text = $("select.relfilter :selected").text(),
		link = $("a.relfilter"),
		filters = {'irrelevant' : 'False',
			   'relevant' : 'True'};

		/*
		 * override default filter, which is to show
		 * only relevant blurbs.
		 */

		/*
		 * Only irrelevant blurbs
		 */
		if (select.val() == 2){
		    filters = {
			'irrelevant' : 'True',
			'relevant' : 'False'
		    };
		/*
		 * Show all blurbs
		 */
		} else if (select.val() == 3){
		    filters = {
			'irrelevant' : 'True',
			'relevant' : 'True'
		    };
		};
		link.html(text).show();
		$.get(link[0].href, filters, function(data) {
			  $("#blurbs").html(data);
			  /* inserting the html blows away jqueries event handlers */
			  bind_event_handlers();
		      });

	    });
    };

    var bind_filter_link = function(){
	/* Show filter options */
	$("a.relfilter").click(
	function(event){
	    $(event.target).hide();
	    $("select.relfilter").show();
	    event.preventDefault();
	});
    };

    var bind_visit_link = function(){
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
    };

    var bind_thumb_button = function(){
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
    };

    bind_event_handlers();
});
