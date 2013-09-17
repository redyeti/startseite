function load() {
	$.get('ajax/getItems', function(data) {
		$('#table').html(data);
	});
}

load();
//window.setInterval(60000, load);

