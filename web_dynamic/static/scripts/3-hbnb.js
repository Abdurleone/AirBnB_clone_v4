$('document').ready(function () {
	const url = 'http://' + window.location.hostname + ':5001/api/v1/status/';
	$.get(url, function (res) {
		if (res.status === 'OK') {
			$('#api_status').addClass('available');
		} else {
			$('#api_status').removeClass('available');
		}
	});
	const url2 = 'http://' + window.location.hostname + ':5001/api/v1/places_search/';
	$.ajax({
		type: 'POST',
		url: url2,
		data: JSON.stringify({
		}),
		success: function (data) {
			for (const place of data.values()) {
				$('.places').append('<article><div class="title"><h2>' + place.name + '</h2><div class="price_by_night">' + place.price_by_night + '</div></div><div class="information"><div class="max_guest"><i class="fa fa-users fa-3x" aria-hidden="true"></i><br />' + place.max_guest + ' Guests</div><div class="number_rooms"><i class="fa fa-bed fa-3x" aria-hidden="true"></i><br />' + place.number_rooms + ' Bedrooms</div><div class="number_bathrooms"><i class="fa fa-bath fa-3x" aria-hidden="true"></i><br />' + place.number_bathrooms + ' Bathroom</div></div><div class="description">' + place.description + '</div></article>');
			}
		},
		error: function (data) {
			console.log('Not Json');
		},
		dataType: 'json',
		contentType: 'application/json'
	});

	const amenities = {};
	$('INPUT[type="checkbox"]').change(function () {
		if ($(this).is(':checked')) {
			amenities[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete amenities[$(this).attr('data-id')];
		}
		$('.amenities H4').text(Object.values(amenities).join(', '));
	});
});
