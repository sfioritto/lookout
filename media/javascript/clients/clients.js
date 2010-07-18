$(document).ready(
function(){

    var update_client = function(container){
	var link = $("a.save", container),
	href = link[0].href,
	id = link[0].id,
	input = $("input.name", container),
	val = input.val();
	$.post(href, {'name' : val,
		      'id' : id});
	$("a.name", container).text(val);
	container.removeClass("edit");
    };

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

    $("a.edit").click(
    function(event){
	$(event.target).parent().parent().addClass("edit");
	event.preventDefault();
    });

    $("a.cancel").click(
    function(event){
	$(event.target).parent().parent().removeClass("edit");
	event.preventDefault();
    });

    $("a.save").click(
    function(event){
	var container = $(event.target).parent().parent();
	update_client(container);
	event.preventDefault();
    });

    $("form.client").submit(
    function(event){
	var container = $(event.target).parent().parent();
	update_client(container);
	event.preventDefault();
    });

});