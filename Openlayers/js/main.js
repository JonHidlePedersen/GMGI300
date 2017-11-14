var map;

function init(){
    var projection = ol.proj.get('EPSG:32633');
    // The extent is used to determine zoom level 0. Recommended values for a
    // projection's validity extent can be found at http://epsg.io/.
    projection.setExtent([-1206118.71, 4021309.92, 1295389.00, 8051813.28]);
    map = new ol.Map({
        target: 'kart',
        renderer: 'canvas',
    	view: new ol.View({
    		projection: projection,
    		center: [261920, 6621680],
    		zoom: 13
    	}) // view
    }); // map

    // Kartlag, definisjoner:
    okartLayer = new ol.layer.Image({
        extent: [-1206118.71, 4021309.92, 1295389.00, 8051813.28],
        //opacity: 0.5,
        source: new ol.source.ImageWMS({
            url: 'http://gis.umb.no/nof/o_kart_wms',
            params: {'layers': 'okart','transparent' : 'true'},
            ratio: 1.2,
            attributions: [
              new ol.Attribution({
                html: '<a href="http://www.orientering.no">Norges Orienteringsforbund</a>'
              }),
            ],
            serverType: 'mapserver'
        }),
        name: 'O-kart WMS'
    }); // okartLayer

    NDLayer = new ol.layer.Image({
        extent: [-1206118.71, 4021309.92, 1295389.00, 8051813.28],
        opacity: 1,
        source: new ol.source.ImageWMS({
            url: 'http://openwms.statkart.no/skwms1/wms.topo2.graatone',
            params: {'LAYERS': 'topo2_graatone_WMS'},
            ratio: 1.1,
            attributions: [
              new ol.Attribution({
                html: '<a href="http://kartverket.no">Kartverket</a>,' +
                      'kommuner, GeoVEKST'
              }),
            ],
            serverType: 'mapserver'
        }),
        name: 'Norge Digitalt topo WMS'
    }); // NDLayer

    // Legg kartlagene pÃ¥ kartet:
    map.addLayer(NDLayer); // bakgrunnskart - legg til fÃ¸rst
    map.addLayer(okartLayer);
} // init