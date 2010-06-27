$(document).ready(function(){

var DEFAULT_VALUE = "Type a new search term here.";


var add_term = function(url){
    var input = $("#addform input")[0];

    /*don't do anything if the input is blank or the default value*/
    if (input.value == DEFAULT_VALUE){
	input.value = "";
    } else if (input.value){
	$.post(url, {
		   'term' : input.value
	       }, function(){
		   $.get('list/', function(data) {
			     $("#alerts").html(data);
			     /* inserting the html blows away jqueries event handlers */
			     bind_delete_links();
			 });
	       });
	input.value = "";
    }
}

var bind_delete_links = function(){
    $("a.delete").click(function(event){
			    var container = $(event.target).parent().parent();
			    $.post(event.target.href, {
				       'id' : event.target.id
				   });
			    container.addClass("disabled");

			    event.preventDefault();
			});

};
/*disable the alert*/
bind_delete_links();

$("#addlink").click(function(event){
			$("#addform, #formlinks").show();
			$(event.target).hide();
			event.preventDefault();
		    });

$("#canceladd").click(function(event){
			  $("#addlink").show();
			  $("#addform, #formlinks").hide();
			  $("#addform input")[0].value = DEFAULT_VALUE;
			  event.preventDefault();
		      });

$("#addterm").click(function(event){
			add_term(event.target.href);
			event.preventDefault();
		    });

$("#addform").submit(function(event){
			 add_term($("#addterm")[0].href);
			 event.preventDefault();
		     });


$("#addform input").focus(function(event){
			      if (event.target.value === DEFAULT_VALUE){
				  event.target.value = "";
			      }
});

$("#addform input").blur(function(event){
			      if (event.target.value == ""){
				  event.target.value = DEFAULT_VALUE;
			      }
});

});