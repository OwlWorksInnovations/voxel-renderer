#version 330
in vec3 in_vert;
in vec3 in_pos;
out vec3 v_pos;

uniform mat4 mvp;

void main() {
    v_pos = in_vert;
    gl_Position = mvp * vec4(in_vert + in_pos, 1.0);
}