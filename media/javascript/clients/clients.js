$(document).ready(
function(){
    	$("a.delete").click(
	function(event){
	    $.post(event.target.href, {
		       'id' : event.target.id
		   });

	    event.preventDefault();
	});

});