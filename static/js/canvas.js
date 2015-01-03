var camera, scene, projector, renderer;
var particleMaterial;
var points_per_shape;
var origin;
var init_angle;
var lines;
var shapes;
var octree;

window.onload = function() {
initScene();
animate();
}

function initOctree(){
    octree = new THREE.Octree({
        radius: 1, // optional, default = 1, octree will grow and shrink as needed
        undeferred: false, // optional, default = false, octree will defer insertion until you call octree.update();
        depthMax: Infinity, // optional, default = Infinity, infinite depth
        objectsThreshold: 8, // optional, default = 8
        overlapPct: 0.15, // optional, default = 0.15 (15%), this helps sort objects that overlap nodes
        scene: scene // optional, pass scene as parameter only if you wish to visualize octree
    } );
}

function initScene() {
	scene = new THREE.Scene();
    //initOctree();
	camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 1, 4000);
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

    labryinth_lines = initLabyrinthTiling();
    curr_labryinth_index_bottom = 0;
    curr_labryinth_index_top = labryinth_lines.length;

}

function bigger(vertices){
    var scale = 1.15;
    var bigger_vertices = [];
    vertices.forEach(function(vertex){
        biggervertex = new THREE.Vector3();
        biggervertex.copy(vertex);
        biggervertex.multiplyScalar(scale);
        bigger_vertices.push(biggervertex);
    });
    return bigger_vertices;
}

function initLabyrinthTiling(){
    labyrinth_lines = [];
    var triangles = [];
    var iterations = 7;
    var vertices = [];
    // start with equilateral triangle
    vertices.push(new THREE.Vector3(-0.5,0,0));
    vertices.push(new THREE.Vector3(0.5,0,0));
    vertices.push(new THREE.Vector3(0,Math.sqrt(0.75),0));
    triangles.push(vertices);
    for (var iter=0; iter<iterations; iter++){
        var new_triangles = [];
        for (var i=0; i<triangles.length; ++i){
            var old_triangle = triangles[i];
            old_triangle = bigger(old_triangle);
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

    for (var i=0; i<triangles.length; i++){
        labyrinth_lines.push.apply(drawVerticesCircular(triangles[i], true));
    }

    return labyrinth_lines;
}

function split_equilateral(triangle_vertices){
    var x = triangle_vertices[0];
    var y = triangle_vertices[1];
    var z = triangle_vertices[2];
    var center = center_of_mass([x,y,z]);
    var triangles = [];
    triangles.push([x,y,center]);
    triangles.push([x,z,center]);
    triangles.push([z,y,center]);
    return triangles;
}

function split_isosceles(triangle_vertices){
    var x = triangle_vertices[0];
    var y = triangle_vertices[1];
    var z = triangle_vertices[2];
    var triangles = [];
    if (fpEqual(x.distanceTo(y),x.distanceTo(z))){
        // hypotenuse is y-z
        var thirdpoints = thirds(y,z);
        var t1= thirdpoints[0];
        var t2 = thirdpoints[1];
        triangles.push([x,y,t1]);
        triangles.push([x,z,t2]);
        triangles.push([x,t1,t2]);
    } else if (fpEqual(y.distanceTo(x),y.distanceTo(z))){
        // hypotenuse is x-z
        var thirdpoints = thirds(x,z);
        var t1= thirdpoints[0];
        var t2 = thirdpoints[1];
        triangles.push([y,x,t1]);
        triangles.push([y,z,t2]);
        triangles.push([y,t1,t2]);
    } else if (fpEqual(z.distanceTo(x),y.distanceTo(z))){
        // hypotenuse is y-x
        var thirdpoints = thirds(y,x);
        var t1= thirdpoints[0];
        var t2 = thirdpoints[1];
        triangles.push([z,y,t1]);
        triangles.push([z,x,t2]);
        triangles.push([z,t1,t2]);
    } else {
        throw "error: in split_isosceles, but not isosceles";
    }
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

function center_of_mass(vectors){
    var center = new THREE.Vector3();
    vectors.forEach(function(vector) {
        center.addVectors(center,vector);
    });
    center.multiplyScalar(1.0/vectors.length);
    return center;
}

function fpEqual(a, b)
{
    var e = 0.000001; //Number.EPSILON didn't work
    var diff = Math.abs(a - b);
    var epsilon = Math.max(Math.abs(a), Math.abs(b)) * e;
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
    return (fpEqual(dxy,dyz) && fpEqual(dxz,dxy));
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
    return (fpEqual(dxy,dyz) || fpEqual(dxz,dxy) || fpEqual(dxz,dyz));
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

function drawVerticesCircular(vertices, labryinth){
    shape = [];
    labryinth = labryinth || false;
    for (var i=0; i<vertices.length-1; i++){
		line = drawLine(vertices[i],vertices[i+1],labryinth);//labryinth = true = draw labryinth
		labyrinth_lines.push(line);
		}
	line = drawLine(vertices[0],vertices[vertices.length-1], labryinth);
	labyrinth_lines.push(line);
	return shape;
}

function drawLine(a,b, labryinth){
    labryinth = labryinth || false; //default value = false
	var lineGeometry = new THREE.Geometry();
	lineGeometry.vertices.push(a);
	lineGeometry.vertices.push(b);
	var line_color;
	var grey = 0xd3d3d3;
	var labryinth_wall = 0x0000ff;
	var labryinth_not_wall = 0xffffff;
	if (!labryinth){
	    line_color = grey;
	} else {
	    if (vEqual(a.x,b.x) || vEqual(a.y,b.y)){
	        p = 0.0; //0.2;//0.05; // 0.01; // 0.1 looks cool
	        line_color = labryinth_wall;
            if (a.y < b.y){
                a.setY(a.y-p);
                b.setY(b.y+p);
            } else if (a.y > b.y){
                a.setY(a.y+p);
                b.setY(b.y-p);
            }
            else if (a.x < b.x){
                a.setX(a.x-p);
                b.setX(b.x+p);
            } else if (a.x > b.x){
                a.setX(a.x+p);
                b.setX(b.x-p);
            }
	    } else {
	        line_color = labryinth_not_wall;
	    }
	}
	var line = new THREE.Line(lineGeometry, new THREE.LineBasicMaterial({color:line_color}));
	//octree.add(line);
	return line;

}

function vEqual(a,b){
    var diff = Math.abs(a - b);
    return (diff < 0.00000000001);
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
    update();

	render();
}

function update(){

    if (curr_labryinth_index_bottom <= curr_labryinth_index_top){
        scene.add(labryinth_lines[curr_labryinth_index_bottom]);
        scene.add(labryinth_lines[curr_labryinth_index_top]);
    }
    curr_labryinth_index_bottom += 1;
    curr_labryinth_index_top -= 1;

}

function render() {
	camera.lookAt( scene.position );

	renderer.render(scene, camera);
}