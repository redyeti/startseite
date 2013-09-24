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

		// update lag display
		$("#lag").replaceWith($(data).find("#lag"));

		while (1) {
			// if there are no new rows left -> remove all old rows
			if (newrows.length == 0) {
				oldrows.fadeOut(400, function(){ $(this).remove()});
				if (oldrows.length > 0) window.flashTitle("Updated!");
				return;
			// if there are no new rows left -> add them to the displayed table
			} else if (oldrows.length == 0){
				newrows.hide().appendTo("#table").fadeIn();
				return;
			// if the two rows are the same -> ignore both
			} else if ($(oldrows[0]).data("eid") == $(newrows[0]).data("eid")) {
				oldrows.shift();
				newrows.shift();
			// if the priority of the old row is lower -> remove old row
			} else if ($(oldrows[0]).data("priority") <= $(newrows[0]).data("priority")) {
				window.flashTitle("Updated!");
				$(oldrows.shift()).fadeOut(400, function(){ $(this).remove()});
			// otherwise log rows and insert new rows before old rows ?!?
			} else {
				window.flashTitle("Updated!");
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

function markElement (ev) {
	var $tr = $(ev.target).closest("tr")
	$.post("ajax/markItem", {id: $tr.data("eid")}, update);
	$tr.data("eid",-1); //invalidate
}
function unmarkElement (ev) {
	var $tr = $(ev.target).closest("tr")
	$.post("ajax/unmarkItem", {id: $tr.data("eid")}, update);
	$tr.data("eid",-1); //invalidate
}

function mouseMove() {
	window.cancelFlashTitle();
}

$("body").on("click", ".hideButton", hideElement);
$("body").on("click", ".markButton", markElement);
$("body").on("click", ".unmarkButton", unmarkElement);
$("body").on("mousemove", mouseMove);

