$(document).ready(function(){
		      /* go to the visit url on the hidden anchor tag instead of the href on the event target*/
		      $("a.blurb, a.textbtn").click(function(event){
							var container = event.currentTarget.parentNode.parentNode;
							var url = $("a.visit", container)[0].href;
							window.location = url;
							event.preventDefault();
					 });

		      /*markt the div as irrelevant and post to the relevance view*/
		      $("a.relevance").click(function(event){

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
