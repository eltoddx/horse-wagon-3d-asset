"""
Blender Script: Early 1900s European Horse-Drawn Cargo Wagon Generator
Creates a game-ready 3D asset in Blender and exports to GLB format.

How to use:
1. Open Blender
2. Go to Scripting tab
3. Create new text file, paste this script
4. Run (Alt+P)
5. Check console for export confirmation
6. Find wagon.glb in your Blender project folder
"""

import bpy
import bmesh
from mathutils import Vector, Matrix
import math

# Clear default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ===== MATERIALS =====
def create_materials():
    """Create wood and iron materials for game asset"""
    
    # Wood material
    wood_mat = bpy.data.materials.new(name="Wood")
    wood_mat.use_nodes = True
    bsdf = wood_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.6, 0.45, 0.25, 1.0)  # Brown
    bsdf.inputs['Roughness'].default_value = 0.8
    bsdf.inputs['Metallic'].default_value = 0.0
    
    # Iron/Metal material
    iron_mat = bpy.data.materials.new(name="Iron")
    iron_mat.use_nodes = True
    bsdf_iron = iron_mat.node_tree.nodes["Principled BSDF"]
    bsdf_iron.inputs['Base Color'].default_value = (0.3, 0.3, 0.32, 1.0)  # Dark gray
    bsdf_iron.inputs['Roughness'].default_value = 0.6
    bsdf_iron.inputs['Metallic'].default_value = 1.0
    
    return wood_mat, iron_mat

# ===== WAGON BED (CARGO AREA) =====
def create_wagon_bed(wood_mat):
    """Create the main wooden cargo bed"""
    
    # Main bed box: 4m x 2m x 1.5m (length x width x height)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, 1.2)
    )
    bed = bpy.context.active_object
    bed.scale = (2, 1, 0.75)
    bed.name = "WagonBed"
    
    # Apply scale
    bpy.context.view_layer.objects.active = bed
    bpy.ops.object.transform_apply(scale=True)
    
    bed.data.materials.append(wood_mat)
    
    return bed

# ===== WAGON FRAME (WOODEN SUPPORT BEAMS) =====
def create_frame_beam(location, scale, wood_mat):
    """Helper to create wooden frame beams"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    beam = bpy.context.active_object
    beam.scale = scale
    beam.data.materials.append(wood_mat)
    bpy.ops.object.transform_apply(scale=True)
    return beam

def create_wagon_frame(wood_mat):
    """Create wooden frame supports under the bed"""
    
    beams = []
    
    # Front and back supports (lengthwise)
    beams.append(create_frame_beam((0, -0.8, 0.5), (2, 0.1, 0.3), wood_mat))
    beams.append(create_frame_beam((0, 0.8, 0.5), (2, 0.1, 0.3), wood_mat))
    
    # Side supports (widthwise)
    beams.append(create_frame_beam((-1.8, 0, 0.5), (0.1, 1.6, 0.3), wood_mat))
    beams.append(create_frame_beam((1.8, 0, 0.5), (0.1, 1.6, 0.3), wood_mat))
    
    # Bottom longitudinal supports
    beams.append(create_frame_beam((0, 0, 0.25), (1.8, 1.4, 0.15), wood_mat))
    
    return beams

# ===== WHEELS =====
def create_wheel(location, iron_mat):
    """Create a single iron wheel with spokes"""
    
    # Outer rim
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.7,
        depth=0.15,
        vertices=32,
        location=location
    )
    rim = bpy.context.active_object
    rim.name = "WheelRim"
    rim.data.materials.append(iron_mat)
    
    # Hub (center)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15,
        depth=0.2,
        vertices=16,
        location=location
    )
    hub = bpy.context.active_object
    hub.name = "WheelHub"
    hub.data.materials.append(iron_mat)
    
    # Spokes (simple representation with torus segments)
    spoke_count = 8
    for i in range(spoke_count):
        angle = (i / spoke_count) * math.pi * 2
        x = location[0] + math.cos(angle) * 0.5
        y = location[1] + math.sin(angle) * 0.5
        z = location[2]
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, y, z)
        )
        spoke = bpy.context.active_object
        spoke.scale = (0.05, 0.35, 0.08)
        spoke.rotation_euler = (0, 0, angle)
        spoke.data.materials.append(iron_mat)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    return rim, hub

def create_wheels(iron_mat):
    """Create all four wheels"""
    wheels = []
    
    # Front left
    wheels.append(create_wheel((-1.5, -1.2, 0.7), iron_mat))
    # Front right
    wheels.append(create_wheel((-1.5, 1.2, 0.7), iron_mat))
    # Back left
    wheels.append(create_wheel((1.5, -1.2, 0.7), iron_mat))
    # Back right
    wheels.append(create_wheel((1.5, 1.2, 0.7), iron_mat))
    
    return wheels

# ===== AXLES & CONNECTORS =====
def create_axles(iron_mat):
    """Create iron axles connecting wheels"""
    
    axles = []
    
    # Front axle
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=2.6,
        vertices=16,
        location=(-1.5, 0, 0.7)
    )
    front_axle = bpy.context.active_object
    front_axle.rotation_euler = (math.pi/2, 0, 0)
    front_axle.name = "FrontAxle"
    front_axle.data.materials.append(iron_mat)
    bpy.ops.object.transform_apply(rotation=True)
    axles.append(front_axle)
    
    # Back axle
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=2.6,
        vertices=16,
        location=(1.5, 0, 0.7)
    )
    back_axle = bpy.context.active_object
    back_axle.rotation_euler = (math.pi/2, 0, 0)
    back_axle.name = "BackAxle"
    back_axle.data.materials.append(iron_mat)
    bpy.ops.object.transform_apply(rotation=True)
    axles.append(back_axle)
    
    return axles

# ===== TONGUE & YOKE (HORSE ATTACHMENT POINT) =====
def create_tongue(wood_mat, iron_mat):
    """Create the wooden tongue and iron fittings for horse attachment"""
    
    # Main tongue beam (where horse would attach)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-2.5, 0, 0.6)
    )
    tongue = bpy.context.active_object
    tongue.scale = (1.2, 0.15, 0.2)
    tongue.name = "Tongue"
    tongue.data.materials.append(wood_mat)
    bpy.ops.object.transform_apply(scale=True)
    
    # Iron ring/connector at tongue end
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.25,
        minor_radius=0.05,
        location=(-3.3, 0, 0.6)
    )
    yoke_ring = bpy.context.active_object
    yoke_ring.rotation_euler = (math.pi/2, 0, 0)
    yoke_ring.name = "YokeRing"
    yoke_ring.data.materials.append(iron_mat)
    bpy.ops.object.transform_apply(rotation=True)
    
    return tongue, yoke_ring

# ===== SIDE RAILINGS =====
def create_railings(wood_mat):
    """Create simple wooden side railings"""
    
    railings = []
    
    # Left side railing posts
    for i in range(3):
        x = -1 + i
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, -1.1, 1.5)
        )
        post = bpy.context.active_object
        post.scale = (0.12, 0.12, 0.6)
        post.name = f"LeftRail_Post_{i}"
        post.data.materials.append(wood_mat)
        bpy.ops.object.transform_apply(scale=True)
        railings.append(post)
    
    # Right side railing posts
    for i in range(3):
        x = -1 + i
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, 1.1, 1.5)
        )
        post = bpy.context.active_object
        post.scale = (0.12, 0.12, 0.6)
        post.name = f"RightRail_Post_{i}"
        post.data.materials.append(wood_mat)
        bpy.ops.object.transform_apply(scale=True)
        railings.append(post)
    
    # Side beams connecting posts
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -1.1, 1.5))
    left_beam = bpy.context.active_object
    left_beam.scale = (2.2, 0.1, 0.1)
    left_beam.name = "LeftRail_Beam"
    left_beam.data.materials.append(wood_mat)
    bpy.ops.object.transform_apply(scale=True)
    railings.append(left_beam)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 1.1, 1.5))
    right_beam = bpy.context.active_object
    right_beam.scale = (2.2, 0.1, 0.1)
    right_beam.name = "RightRail_Beam"
    right_beam.data.materials.append(wood_mat)
    bpy.ops.object.transform_apply(scale=True)
    railings.append(right_beam)
    
    return railings

# ===== ASSEMBLY =====
def build_wagon():
    """Assemble the complete wagon"""
    
    print("🚜 Building horse-drawn wagon...")
    
    # Create materials
    wood_mat, iron_mat = create_materials()
    print("✓ Materials created")
    
    # Build components
    bed = create_wagon_bed(wood_mat)
    frame = create_wagon_frame(wood_mat)
    wheels = create_wheels(iron_mat)
    axles = create_axles(iron_mat)
    tongue, yoke = create_tongue(wood_mat, iron_mat)
    railings = create_railings(wood_mat)
    
    print("✓ All components created")
    
    # Smooth shading for better appearance
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.shade_smooth()
    
    print("✓ Shading applied")
    
    return bed

# ===== EXPORT =====
def export_wagon():
    """Export the wagon as GLB"""
    
    # Select all mesh objects
    bpy.ops.object.select_all(action='SELECT')
    
    # Export path (same directory as Blender file)
    export_path = "wagon.glb"
    
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_draco_mesh_compression=True,
        export_tangents=True,
    )
    
    print(f"✅ Wagon exported to: {export_path}")
    return export_path

# ===== MAIN =====
if __name__ == "__main__":
    print("\n" + "="*60)
    print("BLENDER HORSE-WAGON GENERATOR")
    print("="*60)
    
    # Build the wagon
    build_wagon()
    
    # Export to GLB
    export_wagon()
    
    print("="*60)
    print("DONE! Your wagon is ready for game engines.")
    print("="*60 + "\n")
