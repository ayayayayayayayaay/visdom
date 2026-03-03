/**
 * Copyright 2017-present, The Visdom Authors
 * All rights reserved.
 *
 * This source code is licensed under the license found in the
 * LICENSE file in the root directory of this source tree.
 */

import React, { useEffect, useRef, useState } from 'react';
import Pane from './Pane';

const PointCloudPane = (props) => {
  const { contentID, content } = props;
  const canvasRef = useRef();
  const [isWebGLSupported, setIsWebGLSupported] = useState(true);
  const [camera, setCamera] = useState({
    position: { x: 0, y: 0, z: 5 },
    rotation: { x: 0, y: 0 },
    zoom: 1
  });

  let gl = null;
  let program = null;
  let positionBuffer = null;
  let colorBuffer = null;
  let pointCount = 0;

  // WebGL shaders
  const vertexShaderSource = `
    attribute vec3 a_position;
    attribute vec3 a_color;
    
    uniform mat4 u_modelViewMatrix;
    uniform mat4 u_projectionMatrix;
    uniform float u_pointSize;
    
    varying vec3 v_color;
    
    void main() {
      gl_Position = u_projectionMatrix * u_modelViewMatrix * vec4(a_position, 1.0);
      gl_PointSize = u_pointSize;
      v_color = a_color;
    }
  `;

  const fragmentShaderSource = `
    precision mediump float;
    
    varying vec3 v_color;
    
    void main() {
      // Create circular points
      vec2 coord = gl_PointCoord - vec2(0.5);
      if (length(coord) > 0.5) {
        discard;
      }
      gl_FragColor = vec4(v_color, 1.0);
    }
  `;

  // Initialize WebGL
  const initWebGL = () => {
    const canvas = canvasRef.current;
    if (!canvas) return false;

    gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) {
      setIsWebGLSupported(false);
      return false;
    }

    // Create shaders
    const vertexShader = createShader(gl.VERTEX_SHADER, vertexShaderSource);
    const fragmentShader = createShader(gl.FRAGMENT_SHADER, fragmentShaderSource);
    
    if (!vertexShader || !fragmentShader) return false;

    // Create program
    program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(program));
      return false;
    }

    gl.useProgram(program);

    // Enable depth testing
    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    return true;
  };

  const createShader = (type, source) => {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error('Shader compile error:', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }

    return shader;
  };

  // Load point cloud data
  const loadPointCloud = () => {
    if (!gl || !program || !content.content) return;

    const { points, colors, point_size = 2.0, background_color = '#000000' } = content.content;
    
    if (!points || points.length === 0) return;

    pointCount = points.length;

    // Create position buffer
    positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    const positions = new Float32Array(points.flat());
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

    // Create color buffer
    colorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    const colorData = new Float32Array(colors.flat());
    gl.bufferData(gl.ARRAY_BUFFER, colorData, gl.STATIC_DRAW);

    // Set background color
    const bgColor = hexToRgb(background_color);
    gl.clearColor(bgColor.r, bgColor.g, bgColor.b, 1.0);

    render();
  };

  // Matrix operations
  const createMatrix4 = () => new Float32Array(16);

  const identity = (out) => {
    out[0] = 1; out[1] = 0; out[2] = 0; out[3] = 0;
    out[4] = 0; out[5] = 1; out[6] = 0; out[7] = 0;
    out[8] = 0; out[9] = 0; out[10] = 1; out[11] = 0;
    out[12] = 0; out[13] = 0; out[14] = 0; out[15] = 1;
    return out;
  };

  const perspective = (out, fovy, aspect, near, far) => {
    const f = 1.0 / Math.tan(fovy / 2);
    const nf = 1 / (near - far);
    
    out[0] = f / aspect; out[1] = 0; out[2] = 0; out[3] = 0;
    out[4] = 0; out[5] = f; out[6] = 0; out[7] = 0;
    out[8] = 0; out[9] = 0; out[10] = (far + near) * nf; out[11] = -1;
    out[12] = 0; out[13] = 0; out[14] = 2 * far * near * nf; out[15] = 0;
    return out;
  };

  const translate = (out, a, v) => {
    const x = v[0], y = v[1], z = v[2];
    out[0] = a[0]; out[1] = a[1]; out[2] = a[2]; out[3] = a[3];
    out[4] = a[4]; out[5] = a[5]; out[6] = a[6]; out[7] = a[7];
    out[8] = a[8]; out[9] = a[9]; out[10] = a[10]; out[11] = a[11];
    out[12] = a[0] * x + a[4] * y + a[8] * z + a[12];
    out[13] = a[1] * x + a[5] * y + a[9] * z + a[13];
    out[14] = a[2] * x + a[6] * y + a[10] * z + a[14];
    out[15] = a[3] * x + a[7] * y + a[11] * z + a[15];
    return out;
  };

  const rotateX = (out, a, rad) => {
    const s = Math.sin(rad), c = Math.cos(rad);
    const a10 = a[4], a11 = a[5], a12 = a[6], a13 = a[7];
    const a20 = a[8], a21 = a[9], a22 = a[10], a23 = a[11];
    
    out[0] = a[0]; out[1] = a[1]; out[2] = a[2]; out[3] = a[3];
    out[4] = a10 * c + a20 * s;
    out[5] = a11 * c + a21 * s;
    out[6] = a12 * c + a22 * s;
    out[7] = a13 * c + a23 * s;
    out[8] = a20 * c - a10 * s;
    out[9] = a21 * c - a11 * s;
    out[10] = a22 * c - a12 * s;
    out[11] = a23 * c - a13 * s;
    out[12] = a[12]; out[13] = a[13]; out[14] = a[14]; out[15] = a[15];
    return out;
  };

  const rotateY = (out, a, rad) => {
    const s = Math.sin(rad), c = Math.cos(rad);
    const a00 = a[0], a01 = a[1], a02 = a[2], a03 = a[3];
    const a20 = a[8], a21 = a[9], a22 = a[10], a23 = a[11];
    
    out[0] = a00 * c - a20 * s;
    out[1] = a01 * c - a21 * s;
    out[2] = a02 * c - a22 * s;
    out[3] = a03 * c - a23 * s;
    out[4] = a[4]; out[5] = a[5]; out[6] = a[6]; out[7] = a[7];
    out[8] = a00 * s + a20 * c;
    out[9] = a01 * s + a21 * c;
    out[10] = a02 * s + a22 * c;
    out[11] = a03 * s + a23 * c;
    out[12] = a[12]; out[13] = a[13]; out[14] = a[14]; out[15] = a[15];
    return out;
  };

  const scale = (out, a, v) => {
    const x = v[0], y = v[1], z = v[2];
    out[0] = a[0] * x; out[1] = a[1] * x; out[2] = a[2] * x; out[3] = a[3] * x;
    out[4] = a[4] * y; out[5] = a[5] * y; out[6] = a[6] * y; out[7] = a[7] * y;
    out[8] = a[8] * z; out[9] = a[9] * z; out[10] = a[10] * z; out[11] = a[11] * z;
    out[12] = a[12]; out[13] = a[13]; out[14] = a[14]; out[15] = a[15];
    return out;
  };

  // Render function
  const render = () => {
    if (!gl || !program || pointCount === 0) return;

    const canvas = canvasRef.current;
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Set up matrices
    const projectionMatrix = createMatrix4();
    const modelViewMatrix = createMatrix4();
    
    perspective(projectionMatrix, Math.PI / 4, canvas.width / canvas.height, 0.1, 100.0);
    
    identity(modelViewMatrix);
    translate(modelViewMatrix, modelViewMatrix, [camera.position.x, camera.position.y, -camera.position.z]);
    rotateX(modelViewMatrix, modelViewMatrix, camera.rotation.x);
    rotateY(modelViewMatrix, modelViewMatrix, camera.rotation.y);
    scale(modelViewMatrix, modelViewMatrix, [camera.zoom, camera.zoom, camera.zoom]);

    // Set uniforms
    const projectionLocation = gl.getUniformLocation(program, 'u_projectionMatrix');
    const modelViewLocation = gl.getUniformLocation(program, 'u_modelViewMatrix');
    const pointSizeLocation = gl.getUniformLocation(program, 'u_pointSize');
    
    gl.uniformMatrix4fv(projectionLocation, false, projectionMatrix);
    gl.uniformMatrix4fv(modelViewLocation, false, modelViewMatrix);
    gl.uniform1f(pointSizeLocation, content.content.point_size || 2.0);

    // Set attributes
    const positionLocation = gl.getAttribLocation(program, 'a_position');
    const colorLocation = gl.getAttribLocation(program, 'a_color');

    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    gl.enableVertexAttribArray(colorLocation);
    gl.vertexAttribPointer(colorLocation, 3, gl.FLOAT, false, 0, 0);

    // Draw points
    gl.drawArrays(gl.POINTS, 0, pointCount);
  };

  // Utility functions
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16) / 255,
      g: parseInt(result[2], 16) / 255,
      b: parseInt(result[3], 16) / 255
    } : { r: 0, g: 0, b: 0 };
  };

  // Mouse interaction
  const handleMouseDown = (e) => {
    const startX = e.clientX;
    const startY = e.clientY;
    const startRotationX = camera.rotation.x;
    const startRotationY = camera.rotation.y;

    const handleMouseMove = (e) => {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;
      
      setCamera(prev => ({
        ...prev,
        rotation: {
          x: startRotationX + deltaY * 0.01,
          y: startRotationY + deltaX * 0.01
        }
      }));
    };

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY > 0 ? 1.1 : 0.9;
    setCamera(prev => ({
      ...prev,
      zoom: Math.max(0.1, Math.min(10, prev.zoom * zoomFactor))
    }));
  };

  // Effects
  useEffect(() => {
    if (initWebGL()) {
      loadPointCloud();
    }
  }, []);

  useEffect(() => {
    loadPointCloud();
  }, [content]);

  useEffect(() => {
    render();
  }, [camera]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const resizeCanvas = () => {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        render();
      };
      
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);
      return () => window.removeEventListener('resize', resizeCanvas);
    }
  }, []);

  const handleDownload = () => {
    const canvas = canvasRef.current;
    if (canvas) {
      const link = document.createElement('a');
      link.download = `${contentID}_pointcloud.png`;
      link.href = canvas.toDataURL();
      link.click();
    }
  };

  const resetCamera = () => {
    setCamera({
      position: { x: 0, y: 0, z: 5 },
      rotation: { x: 0, y: 0 },
      zoom: 1
    });
  };

  if (!isWebGLSupported) {
    return (
      <Pane {...props}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          height: '100%',
          color: '#666'
        }}>
          WebGL is not supported in your browser. Point cloud visualization requires WebGL.
        </div>
      </Pane>
    );
  }

  return (
    <Pane
      {...props}
      handleDownload={handleDownload}
      barwidgets={[
        <button key="reset" onClick={resetCamera} className="pull-right" title="Reset Camera">
          ⌂
        </button>
      ]}
    >
      <canvas
        ref={canvasRef}
        style={{ 
          width: '100%', 
          height: '100%', 
          display: 'block',
          cursor: 'grab'
        }}
        onMouseDown={handleMouseDown}
        onWheel={handleWheel}
      />
    </Pane>
  );
};

export default PointCloudPane;