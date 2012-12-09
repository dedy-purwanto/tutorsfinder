function setSelectValueFromText(id, value)
{
	
	$("#"+id+" option:contains('" + value +"')").attr("selected","selected") ;
	

}

function moveTo(address){

    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {

            results_len = results.length
            var results_table = new Array();
            
            geocode_bound = results[0].geometry.bounds;
            
            if (geocode_bound != undefined)
            {
                map.fitBounds(geocode_bound);
            }
            for(i=0; i<results_len; i++){
                address_location = results[i].geometry.location
                
                if(i==0){
                    set_center(address_location.lat(), address_location.lng())
                }
                results_table[i] = '<div style="cursor: pointer" onclick="set_center(' +
                    address_location.lat() + ', ' +
                    address_location.lng() + ');">' +
                    results[i].formatted_address +
                    '</div>';
            }
        
            $('#search_results').html(results_table.join(''));
            
    
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}

function codeAddress(){
    var address = $('#city_country').val();
    moveTo(address);
}


function set_center(lat, lng){
    latlng = new google.maps.LatLng(lat, lng);
    marker.setPosition(latlng)
    map.setCenter(latlng);
    
    geocoder.geocode({'latLng': latlng}, function(results, status) {
    	
    	selectPoint(results);
    	map.fitBounds(results[0].geometry.bounds);
    });

}

function reset_point(loc){
    my_point.setPosition(loc)
    map.setCenter(loc)
}
