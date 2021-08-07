import os
import bpy

from math import radians
from pathlib import Path


def rotate_and_render(
    output_dir,
    output_file_pattern_string = 'render%d.jpg',
    rotation_steps = 8,
    rotation_angle = 360.0,
    subject = bpy.context.object
):
    output_dir = Path(output_dir).resolve()
    original_rotation = subject.rotation_euler
    for step in range(rotation_steps):
        subject.rotation_euler[2] = radians(step * (rotation_angle / rotation_steps))
        bpy.context.scene.render.filepath = os.path.join(output_dir, (output_file_pattern_string % step))
        bpy.ops.render.render(write_still = True)

    subject.rotation_euler = original_rotation