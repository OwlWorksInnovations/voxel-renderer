import pygame
import moderngl
import numpy as np
import glm

def load_shader(path):
    with open(path) as f:
        return f.read()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
    
    # Create context, enable depth_test and load shaders
    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST)
    prog = ctx.program(
        vertex_shader=load_shader("./src/shaders/vertex.glsl"),
        fragment_shader=load_shader("./src/shaders/fragment.glsl"),
    )
    
    # Square (Face) vertices with dtype f4 (float)
    vertices = np.array([
        -0.5, -0.5,  0.5,  # 0 front bottom left
        0.5, -0.5,  0.5,  # 1 front bottom right
        0.5,  0.5,  0.5,  # 2 front top right
        -0.5,  0.5,  0.5,  # 3 front top left
        -0.5, -0.5, -0.5,  # 4 back bottom left
        0.5, -0.5, -0.5,  # 5 back bottom right
        0.5,  0.5, -0.5,  # 6 back top right
        -0.5,  0.5, -0.5,  # 7 back top left
    ], dtype='f4')
    
    # Tells the vertices where to connect to, i4 (int32)
    indices = np.array([
        # Face 1
        0, 1, 2,
        0, 2, 3,
        # Face 2
        0, 1, 5,
        0, 5, 4,
        # Face 3
        1, 2, 6,
        1, 6, 5,
        # Face 4
        3, 2, 6,
        3, 6, 7,
        # Face 5
        0, 3, 7,
        0, 7, 4,
        # Face 6
        7, 6, 5,
        7, 5, 4,
    ], dtype="i4")

    cube_offsets = np.array([
        [x, y, z] 
        for x in range(32) 
        for y in range(32) 
        for z in range(32)
    ], dtype='f4')

    # Sends the vertices to the buffer (gpu)
    vbo = ctx.buffer(vertices)
    ibo = ctx.buffer(indices)
    instance_vbo = ctx.buffer(cube_offsets)
    vao = ctx.vertex_array(prog, [(vbo, '3f', 'in_vert'), (instance_vbo, '3f /i', 'in_pos')], index_buffer=ibo)

    # Set up the camera
    projection = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 2000.0)
    view = glm.lookAt(glm.vec3(60, 60, 50), glm.vec3(16, 16, 16), glm.vec3(0, 1, 0))
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    
    pv = projection * view
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ctx.clear(0.1, 0.1, 0.1, depth=1.0)
        
        prog['mvp'].write(pv)
            
        vao.render(moderngl.TRIANGLES, instances=32768)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
main()