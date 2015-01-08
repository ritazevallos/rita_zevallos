function render() {
	camera.lookAt( scene.position );

	renderer.render(scene, camera);
}

function update(){
    var timer = Date.now() * 0.00001;

    camera.position.x = Math.cos( timer ) * 200;
    camera.position.z = Math.sin( timer ) * 200;
    camera.lookAt( scene.position );
}

function animate() {
	requestAnimationFrame( animate );
    update();

	render();
}

/* sets up scene and adds the canvas to container div #container */
function initScene(){
    // set the scene size
    var WIDTH = window.innerWidth,
      HEIGHT = window.innerHeight;

    // set some camera attributes
    var VIEW_ANGLE = 45,
      ASPECT = WIDTH / HEIGHT,
      NEAR = 0.1,
      FAR = 10000;

    // create a WebGL renderer, camera
    // and a scene
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setClearColor( 0xffffff, 1);
    camera =
      new THREE.PerspectiveCamera(
        VIEW_ANGLE,
        ASPECT,
        NEAR,
        FAR);

    scene = new THREE.Scene();

    // add the camera to the scene
    scene.add(camera);

    // the camera starts at 0,0,0
    // so pull it back
    camera.position.z = 300;

    // start the renderer
    renderer.setSize(WIDTH, HEIGHT);

    // create a point light
    var pointLight =
      new THREE.PointLight(0xFFFFFF);

    pointLight.position.x = 10;
    pointLight.position.y = 50;
    pointLight.position.z = 130;

    scene.add(pointLight);

    projector = new THREE.Projector();
    mouseVector = new THREE.Vector3();
    window.addEventListener( 'mousemove', onMouseMove, false );
    window.addEventListener( 'mouseclick', onMouseClick, false );
    window.addEventListener( 'resize', onWindowResize, false );

    container = $('#container');
    container.hide();
    container.html(renderer.domElement);
    container.fadeIn('slow');
}

function onMouseClick (e ){
    containerWidth = container.clientWidth;links_object
    containerHeight = container.clientHeight;
    mouseVector.x = 2 * (e.clientX / containerWidth) - 1;
    mouseVector.y = 1 - 2 * ( e.clientY / containerHeight );
    var raycaster = projector.pickingRay( mouseVector.clone(), camera );
    if (typeof points_object !== 'undefined' && points_object){
        var intersects_points = raycaster.intersectObjects( points_object.children );

        if (intersects_points.length > 0) {
            var id = intersects_points[0].object.userData.node_id;
            window.open("/node/"+id);
        }
    }
    if (typeof links_object !== 'undefined' && links_object){
        var intersects_links = raycaster.intersectObjects( links_object.children );
        if (intersects_links.length > 0) {
            // identify the path and link to that path
        }
    }
}

function onMouseMove( e ){
    containerWidth = container.clientWidth;
    containerHeight = container.clientHeight;
    mouseVector.x = 2 * (e.clientX / containerWidth) - 1;
    mouseVector.y = 1 - 2 * ( e.clientY / containerHeight );
    var raycaster = projector.pickingRay( mouseVector.clone(), camera );
    if (typeof points_object !== 'undefined' && points_object){
        var intersects_point = raycaster.intersectObjects( points_object.children );

        points_object.children.forEach(function(point){
            point.material.color.set(0xCC0000);
        })

        for( var i = 0; i < intersects_point.length; i++ ) {
            debugger;
            var intersection = intersects_point[ i ],
                obj = intersection.object;

            obj.material.color.setRGB( 265, 265, 265 );
        }
    }
    if (typeof links_object !== 'undefined' && links_object){

        var intersects_link = raycaster.intersectObjects( links_object.children );
        for( var i = 0; i < intersects_link.length; i++ ) {
            var intersection = intersects_link[ i ],
                obj = intersection.object;

            obj.material.color.setRGB( 265, 265, 265 );
        }
    }
}

function onWindowResize( e ) {
        containerWidth = container.clientWidth;
        containerHeight = container.clientHeight;
        renderer.setSize( containerWidth, containerHeight );
        camera.aspect = containerWidth / containerHeight;
}

function loadGraph(url){

    var sphere_template = getSphereTemplate();

    $.get(url,function(data,status){
        if (status=="success"){
            var nodes = JSON.parse(data.nodes);
            var links = JSON.parse(data.links);

            points_object = new THREE.Object3D();
            scene.add(points_object)
            points = {};

            var xRange = 200;
            var yRange = 250;
            var zRange = 200;

            for (var i=0; i<nodes.length; i++){
                node = nodes[i];
                id = node.pk;
                title = node.fields.title;
                x = node.fields.positionX;
                if (x && y && z){
                    var pX = x;
                } else {
                    var pX = Math.random() * xRange - 0.5*xRange,
                    pY = Math.random() * yRange - 0.5*yRange,
                    pZ = Math.random() * zRange - 0.5*zRange;

                    var sphere = sphere_template.clone();
                    sphere.position.set(pX, pY, pZ);
                    sphere.userData = { node_id: id };
                    points_object.add(sphere);

                    points[id] = new THREE.Vector3(pX,pY,pZ);
                }
            }

            links_object = new THREE.Object3D();
            scene.add(links_object);

            for (var i=0; i<links.length; i++){
                link = links[i];
                from = link.fields.from_node; // these correspond to node pks
                to = link.fields.to_node;

                a = points[from];
                b = points[to];
                if (!a || !b){
                    debugger;
                }

                var lineGeometry = new THREE.Geometry();
            	lineGeometry.vertices.push(a);
            	lineGeometry.vertices.push(b);
            	var line_color = 0x000000;
            	var line = new THREE.Line(lineGeometry, new THREE.LineBasicMaterial({color:line_color}));
        	    links_object.add(line);
            }


        } else {
            alert("Error loading graph: "+status);
        }
    });
}

function getSphereTemplate(){
    var radius = 1;
    var sphereMaterial = new THREE.MeshLambertMaterial({color: 0xCC0000});

    return new THREE.Mesh(
      new THREE.SphereGeometry(radius),
      sphereMaterial);
}