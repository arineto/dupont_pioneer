function init_map(map){
  var mapOptions = {
    center: new google.maps.LatLng(42.404803, -82.191038),
    zoom: 13,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };
  map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

  google.maps.event.addListener(map, 'click', function (e) {
    if (drawing==true){
      var currentPath = polygon.getPath();
      currentPath.push(e.latLng);
    }
  });
  return map;
}