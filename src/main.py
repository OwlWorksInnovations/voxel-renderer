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

    # Sends the vertices to the buffer (gpu)
    vbo = ctx.buffer(vertices)
    ibo = ctx.buffer(indices)
    vao = ctx.vertex_array(prog, [(vbo, '3f', 'in_vert')], index_buffer=ibo)

    # Set up the camera
    projection = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 100.0)
    view = glm.lookAt(glm.vec3(2, 2, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t = pygame.time.get_ticks() * 0.001
        
        # Create a model matrix (position, scale, rotation)
        model = glm.mat4(1.0)
        
        # Make cube rotate
        # model = glm.rotate(model, t, glm.vec3(1, 1, 0))
        
        mvp = projection * view * model
        prog['mvp'].write(mvp)
        
        ctx.clear(0.1, 0.1, 0.1, depth=1.0)
        vao.render(moderngl.TRIANGLES)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
main()