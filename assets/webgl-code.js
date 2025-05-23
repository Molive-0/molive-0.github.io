var canvas, gl;
var posAttribute, timeUniform, aspectUniform, mouseUniform;
var prog, rect;
var startTime, currTime, time, aspect;

function glCheck() {
	var err = gl.getError();
	if (err != 0) {
		console.log(err);
	}
}

function getShader(id, type) {
	var shader = gl.createShader(type);
	glCheck();
	var shaderScript = document.getElementById(id);
	gl.shaderSource(shader, shaderScript.innerText);
	glCheck();
	gl.compileShader(shader);
	glCheck();

	if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
		alert(shaderScript.innerText);
		alert(gl.getShaderInfoLog(shader));
	}

	return shader;
}

function setupShaders() {
	var vsh = getShader("vsh", gl.VERTEX_SHADER);
	var fsh = getShader("fsh", gl.FRAGMENT_SHADER);

	prog = gl.createProgram();
	glCheck();
	gl.attachShader(prog, vsh);
	glCheck();
	gl.attachShader(prog, fsh);
	glCheck();
	gl.linkProgram(prog);
	glCheck();

	if (!gl.getProgramParameter(prog, gl.LINK_STATUS))
		alert("Cannot link program");

	gl.useProgram(prog);
	glCheck();

	posAttribute = gl.getAttribLocation(prog, "pos");
	glCheck();
	gl.enableVertexAttribArray(posAttribute);
	glCheck();

	timeUniform = gl.getUniformLocation(prog, "iTime");
	glCheck();
	aspectUniform = gl.getUniformLocation(prog, "aspect");
	glCheck();

	rect = gl.createBuffer();
	glCheck();
	gl.bindBuffer(gl.ARRAY_BUFFER, rect);
	glCheck();

	var verts = [-1, -1, 0, -1, 1, 0, 1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 1, 0];
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
	glCheck();
}

function draw() {

	requestAnimationFrame(draw);
	glCheck();
	//console.log("b");
	currTime = (new Date()).getTime()
	time = (currTime - startTime) / 1500.0;
	aspect = canvas.clientWidth / canvas.clientHeight;
	//console.log("b");
	gl.uniform1f(timeUniform, time);
	glCheck();
	gl.uniform1f(aspectUniform, aspect);
	glCheck();
	gl.clear(gl.COLOR_BUFFER_BIT);
	glCheck();
	//console.log("b");
	gl.bindBuffer(gl.ARRAY_BUFFER, rect);
	glCheck();
	gl.vertexAttribPointer(posAttribute, 3, gl.FLOAT, false, 3 * 4, 0);
	glCheck();
	gl.drawArrays(gl.TRIANGLES, 0, 6);
	glCheck();
	//console.log(gl.getError());
	//console.log("b");
}

function setupWebGL() {
	console.log("a");
	canvas = document.getElementById("bg-live");
	console.log("a");
	canvas.width = canvas.clientWidth / 5;
	canvas.height = canvas.clientHeight / 5;
	console.log("a");
	try { gl = canvas.getContext("webgl"); } catch (e) { }
	if (!gl) alert("Cannot initialize WebGL");
	console.log("a");
	setupShaders();
	console.log("a");
	startTime = (new Date()).getTime();
	console.log("a");
	requestAnimationFrame(draw);
	console.log("a");
}
