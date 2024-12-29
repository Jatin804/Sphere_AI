import http.server
import socketserver
import os
from backend import chat_with_llama

# HTML content with Three.js-based animation
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Three.js Interactive Animation</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <script type="module">
        import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.module.js';

        // Renderer setup
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Scene and camera
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 0, 8);

        // Geometry and material
        const geometry = new THREE.IcosahedronGeometry(2, 10);
        const material = new THREE.MeshBasicMaterial({ 
            color: 0x00ffcc, 
            wireframe: true 
        });

        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // Light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xffffff, 1);
        pointLight.position.set(5, 5, 5);
        scene.add(pointLight);

        // Animation loop
        const clock = new THREE.Clock();
        function animate() {
            const elapsedTime = clock.getElapsedTime();
            mesh.rotation.x = elapsedTime * 0.5;
            mesh.rotation.y = elapsedTime * 0.7;

            // Responsive rendering
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }

        // Handle window resize
        window.addEventListener('resize', () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
        });

        animate();
    </script>
</body>
</html>
"""

# Function to serve the HTML content
def serve_threejs_animation():
    PORT = 8000
    DIRECTORY = "public"

    # Ensure the directory exists
    os.makedirs(DIRECTORY, exist_ok=True)

    # Write the HTML content to a file
    html_file_path = os.path.join(DIRECTORY, "index.html")
    with open(html_file_path, "w") as f:
        f.write(HTML_CONTENT)

    # Define the HTTP handler
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)

    # Start the server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving Three.js animation at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")

if __name__ == "__main__":
    chat_with_llama()
    serve_threejs_animation()
