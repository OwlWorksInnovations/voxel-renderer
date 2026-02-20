#version 330
in vec3 v_pos;
out vec4 f_color;

void main() {
    float edge_width = 0.05;
    vec3 b = abs(v_pos); 

    bool edgeX = b.x > 0.48;
    bool edgeY = b.y > 0.48;
    bool edgeZ = b.z > 0.48;

    if ((edgeX && edgeY) || (edgeX && edgeZ) || (edgeY && edgeZ)) {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        f_color = vec4(0.2, 0.5, 0.8, 1.0);
    }
}