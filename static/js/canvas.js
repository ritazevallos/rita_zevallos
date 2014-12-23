var camera, scene, projector, renderer;
var particleMaterial;
var points_per_shape;
var origin;
var init_angle;
var lines;
var shapes;

window.onload = function() {
initScene();
animate();
}

function initScene() {
	scene = new THREE.Scene();

	camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
	camera.position.z = 3;

	projector = new THREE.Projector();

	renderer = new THREE.WebGLRenderer( { alpha: true });
	renderer.setSize(window.innerWidth, window.innerHeight);
	document.body.appendChild(renderer.domElement);

	objects = [];

	window.addEventListener( 'resize', onWindowResize, false );

	//initSpiralTiling();
	initLight();
	// set the geometry to dynamic
	// so that it allow updates
	//sphere.geometry.dynamic = true;

    initLabyrinthTiling();

}

function initLabyrinthTiling(){
    labryinth_lines = [];
    var triangles = [];
    var iterations = 2;
    var vertices = [];
    // start with equilateral triangle
    vertices.push(new THREE.Vector3(-0.5,1,0));
    vertices.push(new THREE.Vector3(0.5,1,0));
    vertices.push(new THREE.Vector3(0,1+Math.sqrt(0.75),0));
    triangles.push(vertices);
    for (var iter=0; iter<iterations; iter++){
        var new_triangles = [];
        for (var i=0; i<triangles.length; ++i){
            var old_triangle = triangles[i];
            //drawVerticesCircular(triangles[i]);
            console.log("triangle being considered: ");
            console.log(old_triangle);
            if (is_equilateral(old_triangle)){
                new_triangles.push.apply(new_triangles, split_equilateral(old_triangle));
            } else if (is_isosceles(old_triangle)){
                new_triangles.push.apply(new_triangles, split_isosceles(old_triangle));
            } else {
                console.log("Neither equilateral nor isosceles");
                new_triangles.push(old_triangle);
            }
        }
        triangles = new_triangles;
    }

    //drawVerticesCircular(triangles[1]);

    for (var i=0; i<triangles.length; i++){
        drawVerticesCircular(triangles[i]);
    }

}

function split_equilateral(triangle_vertices){
    console.log("in split_equilateral");
    var x = triangle_vertices[0];
    var y = triangle_vertices[1];
    var z = triangle_vertices[2];
    var midXY = midpoint(x,y);
    var center = midpoint(midXY,z);
    var triangles = [];
    triangles.push([x,y,center]);
    triangles.push([x,z,center]);
    triangles.push([z,y,center]);
    return triangles;
}

function split_isosceles(triangle_vertices){
    console.log("in split_isosceles");
    var x = triangle_vertices[0];
    var y = triangle_vertices[1];
    var z = triangle_vertices[2];
    var triangles = [];
    if (x.distanceTo(y) == x.distanceTo(z)){
        // hypotenuse is y-z
        var thirdpoints = thirds(y,z);
        var t1= thirdpoints[0];
        var t2 = thirdpoints[1];
        triangles.push([x,y,t1]);
        triangles.push([x,z,t2]);
        triangles.push([x,t1,t2]);
    } else if (y.distanceTo(x) == y.distanceTo(z)){
        // hypotenuse is x-z
        var thirdpoints = thirds(x,z);
        var t1= thirdpoints[0];
        var t2 = thirdpoints[1];
        triangles.push([y,x,t1]);
        triangles.push([y,z,t2]);
        triangles.push([y,t1,t2]);
    } else if (z.distanceTo(x) == y.distanceTo(z)){
        // hypotenuse is y-x
        var thirdpoints = thirds(y,x);
        var t1= thirdpoints[0];
        var t2 = thirdpoints[1];
        triangles.push([z,y,t1]);
        triangles.push([z,x,t2]);
        triangles.push([z,t1,t2]);
    } else {
        console.log("in split_isosceles, not isosceles");
    }
    console.log("\nsplit triangle");
    console.log(triangle_vertices);
    console.log("into");
    console.log(triangles);
    console.log('\n')
    return triangles;
}

function thirds(x,y){
    var diff = new THREE.Vector3();
    var firstamp = new THREE.Vector3();
    var secondamp = new THREE.Vector3();
    var firstp = new THREE.Vector3();
    var secondp = new THREE.Vector3();
    diff.subVectors(y,x);
    firstamp.copy(diff).multiplyScalar(1/3.0);
    secondamp.copy(diff).multiplyScalar(2/3.0);
    firstp.addVectors(x,firstamp);
    secondp.addVectors(x,secondamp);
    return [firstp, secondp];
}

function midpoint(x,y){
    var center = new THREE.Vector3();
    center.addVectors(x,y).multiplyScalar(0.5);
    return center;
}

function fpEqual(a, b)
{
    var diff = Math.abs(a - b);
    var epsilon = Math.max(Math.abs(a), Math.abs(b)) * Number.EPSILON;
    return (diff < epsilon);
}

function is_equilateral(triangle_vertices){
    if (triangle_vertices.length != 3){
        throw "in is_isosceles: wrong number of vertices";
    }
    var x = triangle_vertices[0];
    var y = triangle_vertices[1];
    var z = triangle_vertices[2];
    var dxy = y.distanceTo(x);
    var dyz = y.distanceTo(z);
    var dxz = x.distanceTo(z);
    if (fpEqual(dxy,dyz) && fpEqual(dxz,dxy)){
        return true;
    } else {
        console.log("Not equilateral. dxy = "+dxy+", dyz = "+dyz+", dxz = "+dxz);
        return false;
    }
}

function is_isosceles(triangle_vertices){
    if (triangle_vertices.length != 3){
        throw "in is_isosceles: wrong number of vertices";
    }
    var x = triangle_vertices[0];
    var y = triangle_vertices[1];
    var z = triangle_vertices[2];
    var dxy = y.distanceTo(x);
    var dyz = y.distanceTo(z);
    var dxz = x.distanceTo(z);
    if (fpEqual(dxy,dyz) || fpEqual(dxz,dxy) || fpEqual(dxz,dyz)) {
        return true;
    } else {
        console.log("Not isosceles. dxy = "+dxy+", dyz = "+dyz+", dxz = "+dxz);
        return false;
    }
}

function initSpiralTiling(){
	console.log('Called initSpiralTiling()');
	points_per_shape = 4;
	lines = [];
	shapes = [initSquare()];
	origin = new THREE.Vector3( 0, 0, 0 );
	// we orient the first shape roughly in the positive quadrant

	var num_shapes = 5;
	var angle_of_rotation = 25 * Math.PI / -180; // rotation is measured in radians
	var scale_of_expansion = 1.8;

	// first shape
	drawShape();

	for (var j=1; j<num_shapes; j++){

		var shape = [];
		previous_shape = shapes[shapes.length-1];
		var axis_of_rotation = new THREE.Vector3(previous_shape[2].x,previous_shape[2].y,1);
		axis_of_rotation.normalize();

		for (var i=0; i<points_per_shape; i++){
			old_vertex = previous_shape[i]; // the most recent shape
			rotated_vertex = new THREE.Vector3();
			rotated_vertex.copy(old_vertex).applyAxisAngle(axis_of_rotation,angle_of_rotation);
			scaled_vertex = rotated_vertex.multiplyScalar(scale_of_expansion);
			shape.push(scaled_vertex);
		}
		shapes.push(shape);
		drawShape(); // draw the most recent shape

	}
	console.log(vertices);
}

function initSquare(){
	console.log('Called initSquare()');
	vertices = [];
	lower_left = new THREE.Vector3( 0, 0, 0 );
	upper_left = new THREE.Vector3( 0, 1, 0 );
	upper_right = new THREE.Vector3( 1, 1, 0 );
	lower_right = new THREE.Vector3( 1, 0, 0 );
	offset = new THREE.Vector3( 0.2, 0.2, 0 );
	vertices.push(lower_left.add(offset));
	vertices.push(upper_left.add(offset));
	vertices.push(upper_right.add(offset));
	vertices.push(lower_right.add(offset));
	return vertices;
}

/* draw the latest shape */
function drawShape(){
	console.log('in drawShape');
	try{
		var shape = shapes[shapes.length-1];
        drawVerticesCircular(shape);
	}
	catch(err){
		alert('Error in drawShape: ' + err.message);
	}
}

function drawVerticesCircular(vertices){
    for (var i=0; i<vertices.length-1; i++){
		drawLine(vertices[i],vertices[i+1]);
		}
	drawLine(vertices[0],vertices[vertices.length-1]);
}

function drawLine(a,b){

	try{
		var lineGeometry = new THREE.Geometry();
		lineGeometry.vertices.push(a);
		lineGeometry.vertices.push(b);
		var line = new THREE.Line(lineGeometry, new THREE.LineBasicMaterial({color:0xd3d3d3}));
		labryinth_lines.push(line);
		scene.add(line);
	}

	catch(err){
		console.log('Error in drawLine: ' + err.message);
	}

}

function initLight(){
	// create a directionalLight
	var directionalLight =
	  new THREE.DirectionalLight( 0xFFFFFF, 0.8 );

	// set its position
	directionalLight.position.x = 20;
	directionalLight.position.y = 0;
	directionalLight.position.z = 40;

	// add to the scene
	scene.add(directionalLight);
}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {
	requestAnimationFrame( animate );

	render();
}

function render() {
	camera.lookAt( scene.position );

	renderer.render(scene, camera);
}