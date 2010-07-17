$(document).ready(
function(){
    	$("a.delete").click(
	function(event){
	    var answer = confirm("Are you sure? You can't undo this.");
	    if (answer){
		$.post(event.target.href, {
			   'id' : event.target.id
		       }, function(){
			   $(event.target).parent().parent().remove();
		       });
	    }
	    event.preventDefault();
	});

});