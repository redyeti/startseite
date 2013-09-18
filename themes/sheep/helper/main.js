jQuery.fn.reverse = [].reverse;
jQuery.fn.shift = [].shift;

function load() {
	$.get('ajax/getItems', function(data) {
		$('#table').empty().append($(data).find("tr"));
		$('#table').after($(data).find("#lag"));
	});
}

load();

function update() {
	$.get('ajax/getItems', function(data) {
		var oldrows = $('#table tr');
		var newrows = $('<table>'+data+'</table>').find('tr');

		$("#lag").replaceWith($(data).find("#lag"));

		while (1) {
			if (newrows.length == 0) {
				oldrows.fadeOut(400, function(){ $(this).remove()});
				return;
			} else if (oldrows.length == 0){
				newrows.hide().appendTo("#table").fadeIn();
				return;
			} else if ($(oldrows[0]).data("eid") == $(newrows[0]).data("eid")) {
				oldrows.shift();
				newrows.shift();
			} else if ($(oldrows[0]).data("priority") <= $(newrows[0]).data("priority")) {
				$(oldrows.shift()).fadeOut(400, function(){ $(this).remove()});
			} else {
				console.log(oldrows, newrows, $(oldrows[0]));
				$(oldrows[0]).before(newrows.shift());
			}	
		}
	}).error(function(){
		$("#lag").text("Server nicht erreichbar.").addClass("error");
	});
}

window.setInterval(update, 10000);

function hideElement (ev) {
	$.post("ajax/hideItem", {id: $(ev.target).closest("tr").data("eid")}, update);
}

$("body").on("click", ".hideButton", hideElement);
