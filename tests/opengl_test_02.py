import OpenGL.GL as gl          #OpenGL
from pyglfw.libapi import *     # Window Toolkit - GLFW (Python libapi version)
import struct
import ctypes

glfwInit()

print(glfwGetVersion())

glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

width = 600
height = 480
window = glfwCreateWindow(width, height, b'Hello GLFW (libapi)', None, None)

glfwMakeContextCurrent(window)

glfwSetInputMode(window, GLFW_STICKY_MOUSE_BUTTONS, gl.GL_TRUE)

def load_shaders():    
    program  = gl.glCreateProgram()

    vertex_shader   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

    shader_file = open('VertexShader.glsl', 'r')        # open the file for reading
    vertex_shader_code = shader_file.read()             # read the whole file
    shader_file.close()                                 # close the file
    gl.glShaderSource(vertex_shader, vertex_shader_code)       # make that the source code

    shader_file = open('FragmentShader.glsl', 'r')
    fragment_shader_code = shader_file.read()
    gl.glShaderSource(fragment_shader, fragment_shader_code)
    shader_file.close()

    # Compile shaders
    gl.glCompileShader(vertex_shader)
    if gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:    # Check if compilation was successful
        info_log = gl.glGetShaderInfoLog(vertex_shader)
        raise RuntimeError('Vertex shader compilation failed: %s' % (info_log))
    else:
        print('Vertex shader compiled successfuly')

    gl.glCompileShader(fragment_shader)
    if gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:    # Check if compilation was successful
        info_log = gl.glGetShaderInfoLog(fragment_shader)
        raise RuntimeError('Fragment shader compilation failed: %s' % (info_log))
    else:
        print('Fragment shader compiled successfuly')

    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)

    gl.glLinkProgram(program)

    gl.glDetachShader(program, vertex_shader)
    gl.glDetachShader(program, fragment_shader)

    return program

#dark blue background
gl.glClearColor(0.0, 0.0, 0.4, 0.0);

# Get our shader program
program = load_shaders()

# Define some data, we will be drawing a triangle
vertices = [-1.0, -1.0,  0.0,
             0.0, +1.0,  0.0,
            +1.0, -1.0,  0.0]

data = (gl.GLfloat * len(vertices))(*vertices)

vertex_array_object = gl.glGenVertexArrays(1)
gl.glBindVertexArray(vertex_array_object)

gl.glUseProgram(program)

# Create a buffer object
buffer = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glBufferData(gl.GL_ARRAY_BUFFER, (4*8)*3*3, data, gl.GL_STATIC_DRAW)     

gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))

# Unbind the VAO
gl.glBindVertexArray(0)

while True:
    # Check the exit condition
    if glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
        break

    # Clear the screen
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);

    # Draw our triangle
    gl.glBindVertexArray(vertex_array_object)
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)         #Starting from vertex 0, draw 3 vertices total -> 1 triangle
    gl.glBindVertexArray(0)

    glfwSwapBuffers(window)
    glfwPollEvents()

glfwTerminate()