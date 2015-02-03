


function message_warn(msg){
	var element = "";
	element += "<div class='alert alert-warning alert-dismissable'>";
	element += "<button type='button' data-dismiss='alert' aria-hidden='true' class='close'>&times;</button>"
	element += "<strong>Warning! </strong>"+msg
	element += "</div>"
	$('#messages').prepend(element)
}

function message_info(msg){
	var element = "";
	element += "<div class='alert alert-success alert-dismissable'>";
	element += "<button type='button' data-dismiss='alert' aria-hidden='true' class='close'>&times;</button>"
	element += "<strong>Well done! </strong>"+msg
	element += "</div>"
	$('#messages').prepend(element)
}

function message_error(msg){
	var element = "";
	element += "<div class='alert alert-danger alert-dismissable'>";
	element += "<button type='button' data-dismiss='alert' aria-hidden='true' class='close'>&times;</button>"
	element += "<strong>Oh snap! </strong>"+msg
	element += "</div>"
	$('#messages').prepend(element)
}

