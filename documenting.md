# Start

## What is opengl?

I learned that opengl just uses shaders which is the gpu programming language (I think) to do operation that require parallel processing like graphics.

## ModernGL

ModernGL has this workflow (after creating context): Write shader code > send to buffer > send to pygame window. I highly recommend using a dedicated shaders folder then installing glsl lint and writing a shader loader (just open the file and return the read).

## 3D Graphics

### Square (2D)

Essentially how every thing in graphics is rendered by using triangles which are constructed of vertices (think of a outline of points) and told where to be drawn using indices (think of how you would fit the triangle).

For example a square (2D) would have vertices of:

```
-0.5, -0.5,  0.5,  # bottom left
0.5, -0.5,   0.5,  # bottom right
0.5,  0.5,   0.5,  # top right
-0.5,  0.5,  0.5,  # top left
```

And here would be its indices:

```
0, 1, 2,
0, 2, 3,
```

And a visual representation:

```
3 ------- 2
|       / |
|     /   |
|   /     |
| /       |
0 ------- 1
```

### Cube (3D)

3D graphics maintains the same concept but you can think of a square being a face because you would need 6 faces to form a cube.

So the vertices for a cube would look like this:

```
-0.5, -0.5,  0.5,  # 0 front bottom left
0.5, -0.5,   0.5,  # 1 front bottom right
0.5,  0.5,   0.5,  # 2 front top right
-0.5,  0.5,  0.5,  # 3 front top left
-0.5, -0.5, -0.5,  # 4 back bottom left
0.5, -0.5,  -0.5,  # 5 back bottom right
0.5,  0.5,  -0.5,  # 6 back top right
-0.5,  0.5, -0.5,  # 7 back top left
```

And the indices

```
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
```

And here is a visual representation

```
    7 ------- 6
   /|        /|
  4 ------- 5 |
  | |       | |
  | 3 ------| 2
  |/        |/
  0 ------- 1
```

Now that we have the cube mapped out we can start to draw it onto the screen. To do this we must first set up a camera with a perspective (think of it being fov settings). After doing that we can then use PyGLM to create a model matrix (Position, scale, rotation) to set the position of the cube in our 3d space. To find out where to put it we use this `mvp = projection * view * model` which reads right to left. The view then shifts the cube relative to the camera (view), and then finally squashed into a 2D perspective.

Resulting in a 3d cube being rendered! If we want to move the cube we simply do the following `model = glm.rotate(model, t, glm.vec3(1, 1, 0))`
