import os
import time
import viser

def main():
    host = os.getenv("VISER_HOST", "0.0.0.0")
    port = int(os.getenv("VISER_PORT", "8082"))
    server = viser.ViserServer(host=host, port=port)
    server.scene.add_frame("/world", show_axes=True, axes_length=0.5, axes_radius=0.01)
    server.scene.add_grid("/ground", width=10, height=10)
    # Simple visual placeholder for humanoid categories. Replace with URDF/mesh imports
    # and live joint/sensor data for a real robot digital twin.
    server.scene.add_frame("/robot/base", show_axes=True, axes_length=0.35, axes_radius=0.015)
    server.scene.add_frame("/robot/torso", show_axes=True, axes_length=0.25, axes_radius=0.012,
                           position=(0.0, 0.0, 1.0))
    server.scene.add_frame("/robot/head", show_axes=True, axes_length=0.18, axes_radius=0.01,
                           position=(0.0, 0.0, 1.55))
    server.scene.add_frame("/robot/left_arm", show_axes=True, axes_length=0.2, axes_radius=0.01,
                           position=(0.0, 0.35, 1.1))
    server.scene.add_frame("/robot/right_arm", show_axes=True, axes_length=0.2, axes_radius=0.01,
                           position=(0.0, -0.35, 1.1))
    print(f"Viser scene available on http://{host}:{port}")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
