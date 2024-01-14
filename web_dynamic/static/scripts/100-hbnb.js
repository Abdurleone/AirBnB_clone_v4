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
		data: '{}',
		dataType: 'json',
		contentType: 'application/json',
		success: addplace
	});

	const amenities = {};
	$('.amenities INPUT[type="checkbox"]').change(function () {
		if ($(this).is(':checked')) {
			amenities[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete amenities[$(this).attr('data-id')];
		}
		$('.amenities H4').text(Object.values(amenities).join(', '));
	});

	const states = {};
	$('.locations > UL > H2 > INPUT[type="checkbox"]').change(function () {
		if ($(this).is(':checked')) {
			states[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete states[$(this).attr('data-id')];
		}
		const locations = Object.assign({}, states, cities);
		if (Object.values(locations).length === 0) {
			$('.locations H4').html('&nbsp;');
		} else {
			$('.locations H4').text(Object.values(locations).join(', '));
		}
	});

	const cities = {};
	$('.locations > UL > UL > LI > INPUT[type="checkbox"]').change(function () {
		if ($(this).is(':checked')) {
			cities[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete cities[$(this).attr('data-id')];
		}
		const locations = Object.assign({}, states, cities);
		if (Object.values(locations).length === 0) {
			$('.locations H4').html('&nbsp;');
		} else {
			$('.locations H4').text(Object.values(locations).join(', '));
		}
	});

	const url3 = 'http://' + window.location.hostname + ':5001/api/v1/places_search/';
	$('button').click(function () {
		$.ajax({
			url: url3,
			type: 'POST',
			data: JSON.stringify({
				amenities: Object.keys(amenities),
				states: Object.keys(states),
				cities: Object.keys(cities)
			}),
			contentType: 'application/json',
			dataType: 'json',
			success: addplace
		});
	});
});
function addplace (data) {
	$('section.places').empty();
	$('section.places').append(data.map(place => {
		return `<article><div class="title"><h2>${place.name}</h2><div class="price_by_night">${place.price_by_night}</div></div><div class="information"><div class="max_guest"><i class="fa fa-users fa-3x" aria-hidden="true"></i></br>${place.max_guest} Guests</div><div class="number_rooms"><i class="fa fa-bed fa-3x" aria-hidden="true"></i></br>${place.number_rooms} Bedrooms</div><div class="number_bathrooms"><i class="fa fa-bath fa-3x" aria-hidden="true"></i></br>${place.number_bathrooms} Bathrooms</div></div><div class="description">${place.description}</div></article>`;
	}));
}
