$(document).ready(function(){
		      $("a.blurb, a.textbtn").click(function(event){
							var container = event.currentTarget.parentNode.parentNode;
							var url = $("a.visit", container)[0].href;
							window.location = url;
							event.preventDefault();
					 });
});
