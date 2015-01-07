/* usage- outer_class: begin / complete / read
          wrapper_id: begin_wrapper / complete_<beginning_id>_wrapper / ending_<ending_id>_wrapper
        url: "complete/<beginning_id>/" /
          */
function loadItem(outer_class,wrapper_id,url,footer){
    //todo: index optional parameter
    var new_section = $('.template').first().clone();
    new_section.addClass(outer_class);
    new_section.removeClass('template');
    new_section.removeClass('active');
    var item = new_section.find('.item').first();
    item.attr('id',wrapper_id);
    if (footer){
        footer.addClass('footer');
        item.after(footer);
    }
    $('#fullpage').append(new_section);
    var curr_wrapper = $('#'+wrapper_id);
    curr_wrapper.load(url, function(){
        curr_wrapper.fadeIn('slow');
    });
}

function loadStart(){
    footer = $('<div />', {
        text: "Press <Enter> to save."
    });
    loadItem("start","begin_wrapper","begin/", footer);
}

function removeAllWithClass(className){
    $('.'+className).fadeOut('slow',function(){
        if ($(this).hasClass('active')){ // todo: change to while, move to next section, and switch to infinite
            //shuffleSections();
            $.fn.fullpage.moveTo(0,0);
        }
        $(this).remove();
    });
}

function goToFirstOfClass(className){
    if ($('.'+className).length ) {
        while (!($('.'+className).hasClass('active'))){
            $.fn.fullpage.moveSectionDown();
        }
    }
}


function loadDefaultSettings(){
    // These are the default settings that the index view
    // loads in. For testing, we're showing all of them, but
    // eventually the default will be to only have the reads.

    $('#startCheckbox').prop('checked', default_start);
    $('#completeCheckbox').prop('checked', default_complete);
    $('#readCheckbox').prop('checked', default_read);
    $('#scrambleCheckbox').prop('checked', false);
}

/* would use this if you are adding more things to the list */
function shuffleSections(){
    var parent = $("#fullpage");
    var divs = parent.children();
    while (divs.length) {
        parent.append(divs.splice(Math.floor(Math.random() * divs.length), 1)[0]);
    }
}

function loadTemplate(lat1,lng1,lat2,lng2){
    var new_section =
        '<div class="section template">'+
            '<div class="item">'+
                '<div class="beginning">'+
                    'Because the world is round, '+
                    '<span class="hidden hidden-lat">' +
                    lat1 +
                    '</span>'+
                    '<span class="hidden hidden-lng">'+
                    lng1 +
                    '</span>'+
                '</div>'+
                '<div class="ending">'+
                    'Love is old, love is new'+
                    '<span class="hidden hidden-lat">'+
                    lat2 +
                    '</span>'+
                    '<span class="hidden hidden-lng">'+
                    lng2 +
                    '</span>'+
                '</div>'+
            '</div>'+
        '</div>';
    $('#fullpage').append(new_section);
}

function loadComplete(beginning_id){
    footer = $('<div />', {
        text: "Press <Enter> to save."
    });
    loadItem("complete", 'complete_'+beginning_id+'_wrapper', "complete/"+beginning_id+"/", footer);
}

function loadScrambled(beginning_id,ending_id){
    loadItem('read','scrambled_'+beginning_id+'_'+ending_id+'_wrapper', 'scrambled/'+beginning_id+'/'+ending_id+'/');
}

function loadEnding(ending_id){
    loadItem("read", 'ending_'+ending_id+'_wrapper', "ending/"+ending_id+"/");
}


function updateGlobeFromSection(section_index,earth,marker1,marker2){
    $.fn.filterByData = function(prop, val) {
        return this.filter(
            function() { return $(this).data(prop)==val; }
        );
    }
    var section = $('.section').filterByData('section_id',section_index).first();
    if (section.hasClass('read')){
        var begin_lat = section.find('.beginning').first().find('.hidden-lat').text();
        var begin_lng = section.find('.beginning').first().find('.hidden-lng').text();
        var end_lat = section.find('.ending').first().find('.hidden-lat').text();
        var end_lng = section.find('.ending').first().find('.hidden-lng').text();
        if (begin_lat != "" && begin_lng != ""){
            marker1.setLatLng([begin_lat, begin_lng]);
            earth.panTo([begin_lat,begin_lng],{'duration':'fast'});
            if (end_lat != "" && end_lng != ""){
                earth.panTo([end_lat,end_lng],{'duration':'fast'});

                marker2.setLatLng([end_lat, end_lng]);
                //marker.bindPopup('<b>Hello world!</b>');
                //var options = {color: '#fff', opacity: 1, fillOpacity: 0.1, weight: 2};
                //var polygonB = WE.polygon([[begin_lat, begin_lng], [end_lat, end_lng], [0,0]], options).addTo(earth);
            } else {
                marker2.setLatLng([begin_lat, begin_lng]);
            }
        }
    }
}

function loadFullpage(earth,marker1,marker2){
    $('#fullpage').fullpage({

        //Scrolling
        css3: true,
        scrollingSpeed: 500,
        autoScrolling: true,
        easing: 'easeInQuart',
        easingcss3: 'ease',
        continuousVertical: true,
        normalScrollElements: '#element1, .element2',
        scrollOverflow: true,
        touchSensitivity: 15,
        normalScrollElementTouchThreshold: 5,

        //Accessibility
        keyboardScrolling: true,
        animateAnchor: true,

        //Design
        controlArrows: true,
        verticalCentered: true,
        resize : false, // this really, really breaks anything bc dynamic
        paddingTop: '3em',
        paddingBottom: '10px',
        fixedElements: '#header, .footer',
        responsive: 0,

        //Custom selectors
        sectionSelector: '.section',
        slideSelector: '.slide',

        //events
        onLeave: function(index, nextIndex, direction){
            // changing map here so it'll be ready
            updateGlobeFromSection(nextIndex,earth,marker1,marker2);
        },
        afterLoad: function(anchorLink, index){
            //alert("afterLoad()");
        },
        afterRender: function(){},
        afterResize: function(){},
    });
}

function setupArrowHandlers(){
    $("#uparrow").mouseenter(function(){
        $.fn.fullpage.moveSectionUp();
    })
    $("#downarrow").mouseenter(function(){
        $.fn.fullpage.moveSectionDown();
    })
}

/* well i broke this somehow but it's not important so i'm just not worrying about it */
function zipString(lat,lng){
    var zip_text = ""; // default in case it doesn't work
    var point = new google.maps.LatLng(lat, lng);
    new google.maps.Geocoder().geocode({'latLng': point}, function (res, status) {
        if (status == google.maps.GeocoderStatus.OK && typeof res[0] !== 'undefined') {
            var zip = res[0].formatted_address.match(/,\s\w{2}\s(\d{5})/);
            if (zip){
                var zip_text = '<br>Zip code: ' + zip[1];
            }
        }
    });
    return zip_text;
}

function renderGeo(earth,lat,lng){
    $('#hidden_lat_container').text(lat);
    $('#hidden_lng_container').text(lng);
    earth.panTo([lat,lng]);
    var info_html = "Latitude: " + lat +
        "<br>Longitude: " + lng + zipString(lat,lng);
    $('#geolocation').html(info_html);
}

function loadGeo(earth){
    var lat;
    var lng;

    if ($('#useGeoButton').is(':checked')){
        $('#geolocation').html("Loading geolocation...");
        info_html = "Geolocation is not supported by this browser."; // default
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position){
                lat = position.coords.latitude;
                lng = position.coords.longitude;
                renderGeo(earth,lat,lng);
            });
        }
    } else if ($('#useRandomGeoButton').is(':checked')){
        lat = Math.random() * 180 - 90.0;
        lng = Math.random() * 360 - 180.0;
        renderGeo(earth,lat,lng);
    } else {
        throw "Neither userGeoButton or useRandomGeoButton are selected."
    }
}

function initGlobe(){
    var options = {
        atmosphere: true,
        center: [0, 0],
        zoom: 1.5,
        zooming:false,
    };
    var earth = new WE.map('earth_div', options);
    WE.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg', {
      subdomains: '1234',
      attribution: 'Tiles Courtesy of MapQuest'
    }).addTo(earth);

    loadGeo(earth);

    return earth;
}

function moveTemplateToTop(){
    var template = $('.template').first();
    template.remove();
    $('#fullpage').prepend(template);
}

function setupGeoButtonHandlers(earth){
    $("#useGeoButton, #useRandomGeoButton").change(function () {
        loadGeo(earth);
    })
}

function addDataIdsToSections(){
    var section_index_counter = 1;
    $(".section").each(function( index, value ){
        $(this).data("section_id",section_index_counter);
        section_index_counter += 1;
    })
}