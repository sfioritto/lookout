$(document).ready(function(){
    /*disable the alert*/
    $("a.delete").click(function(event){
			    var container = $(event.target).parent().parent();
			    $.post(event.target.href, {
				       'id' : event.target.id
				   });
			    container.addClass("disabled");

			    event.preventDefault();
			});

});