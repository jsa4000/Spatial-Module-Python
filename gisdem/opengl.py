
import OpenGL.GL as GL
import OpenGL.GL.shaders
import ctypes
import pygame
import os
import numpy as np
import pandas as pd


# Great useful resource to learn OpenGL and all the concepts needed for understanding
# ligths, materials, shaders, transformations, etc..
# URL: https://learnopengl.com/

"""

https://gamedev.stackexchange.com/questions/92832/in-opengl-whats-quicker-lots-of-smaller-vaos-or-one-large-one-updated-each-fr
https://www.opengl.org/discussion_boards/showthread.php/197893-View-and-Perspective-matrices
https://www.gamedev.net/topic/609159-would-like-help-with-glulookat-and-python-code/


http://pyopengl.sourceforge.net/documentation/manual-3.0/gluLookAt.html
http://stackoverflow.com/questions/3380100/how-do-i-use-glulookat-properly
http://stackoverflow.com/questions/15006905/how-do-i-modify-the-perspective-of-an-opengl-using-glulookat
http://stackoverflow.com/questions/26949617/pyopengl-glulookat-behaviour
http://stackoverflow.com/questions/19078620/rotate-cube-to-look-at-mouse-from-python-in-opengl
"""

def cube3D(origin = [0.0,0.0,0.0], transform = None):
    """
        This function will return a cube using normalized units in
        worl space. You can transform the oject by performing a
        transformation later.
        Also the position of he object by default will be the origin
        of the scene, in this case [0,0,0]
        In general the position will be defined in 4D position, since the
        transformation matrix need to be in 4-dimension to allow the trans-
        lation too. The fourth value will be always 1.0.
    """
    # In order to create a cube or any other 3D geoemtry it's needed
    # to store all the information previousl in a buffer. This buffer
    # will be created and managed by opengl so at the end will be used
    # to represent the content of the buffer into the scene. 
    # I addition to this it's needed to create Shaders (vertex and
    # fragment) so the graphics card can use to know what it's needed
    # prior to represent the data.
    # At the end, we are just defining attributes. But in this 
    # particular case the first attribute that will be defined it's the
    # position. After the position we can define: vertex color, pscale,
    # normals, etc...
    # A cube will have a total of 8 vertices
    # 
    #      2    3
    #      1    0
    #
    vertices = [
        # First we represent the vertices on the bottom y = -1
        1.0, -1.0, -1.0, # right, bottom, front vertex. (0)
        -1.0, -1.0, -1.0, # left, bottom, front vertex. (1)
        -1.0, -1.0, 1.0, # right, bottom, back vertex. (2)
        1.0, -1.0, 1.0, # left, bottom, back vertex. (3)
        # The same vertex positions but on the top of the cube Y= 1
        1.0, 1.0, -1.0, # right, bottom, front vertex. (0)
        -1.0, 1.0, -1.0, # left, bottom, front vertex. (1)
        -1.0, 1.0, 1.0, # right, bottom, back vertex. (2)
        1.0, 1.0, 1.0 # left, bottom, ack vertex. (3)
    ]
    #Conver the array into a numpy array (copy vs reference)
    nvertices = np.asarray(vertices, dtype=np.float32)
    # Defne the elements, in opengl it's needed to define triangles.
    # For each triangle we need to use 3 points or three vertices.
    # In this case we are going to define the indices, that corresponds
    # with the indexes of the vertices in the previos array. 
    # A cube has a total of 6 faces: 4 for the sides + top + bottom.
    # However, we have to define triangles, so each face will be divided
    # by two. At the end we need 6 * 2 = 12 triangles in total
    # The trianglulation will be made in clockwise way. This is important
    # to know where the faces will be facing for shading them (normals).
    indices = [
        0, 1, 2, # Bottom face
        2, 3, 0,
        0, 1, 3, # Front face
        3, 4, 0,
        1, 2, 6, # left side
        6, 3, 1,
        2, 3, 7, # back face
        7, 6, 2,
        3, 0, 4, # Right Side
        4, 7, 3,
        4, 5, 6, # Top face
        6, 7, 4
    ]
    #Conver the array into a numpy array (copy vs reference)
    nindices = np.asarray(indices, dtype=np.int32)
    # The vertices are not repeated. You can have the vertices repeated if
    # you need different attrbiutes for them, like the normals, This will
    # be used to shade the elements in different ways. In some programs
    # This is called vertex normals. An it's used to crease or decrease
    # the weight for the transition between face to face. It's like define
    # smooth areas between the hard-surface areas.
    
    # It will return a tuple with the vertices and indices.
    return (nvertices,nindices)

def empty(value):
    """
        Ths function will return is some list or variable is empty.
        For list, dict or any other collection will check there is 
        more that one element. For other variables the condition
        will check if the object is None.
    """    
    if isinstance(value, (list, dict, np.ndarray, tuple, set)):
        if len(value) > 0:
            return False
    else:
        if value is not None:
            return False
    return True

def isfile(filename):
    """
        Check if file exists
    """
    if os.path.isfile(filename):
        return True
    return False

def readfile(filename):
    """
        Read the current file entirely and return a 
        string variable with all the content with
        special characters like new_line, etc..
    """
    result = None
    if isfile(filename):
        with open(filename,'r') as file:
            result = file.read()
    return result

"""
 For my OpenGL I will need the following classes or objects.

    [DONE] Display: window that manage the 3D view and Input Events 
             fom the user. Also this class will be the one that
             implement the main loop for all the render.
                        
    Shader: This class will be enable the creation of shaders
            programs that will be added to the main shader program
            that will be used.
            We can create Vertex, Fragment or Geoemtry shaders. These
            will be inked and use every time we want to render the
            geometry. 
    Geometry: The class will be the main container for storing
            vertices, indices (element), vertex colors, normals and
            other attributes. Also the geometry will manage the uvs
            attributes and the materials that will be used for this
            particular geoemtry.
                - Vertices/Points
                - Indices (Faces)
                - Attributes (list with the Attrbiutes)
                    Default attributes like Cd, N, P Uv could be 
                    created automatically for each object since they
                    are used by default in all the 3D applications.

    Material: Each geoemtry obejct could have more that one material.
            In this case we have to decide if we are going to use
            different shaders or only one for the entire geometry.
    Camera: This class will allow the creation of different cameras
            to swtich indide the progrm. The camera will configure
            the View and Projection matrix.

    Light:  Every scene have a light to lit the objects. These
            lights will be passed to the shaders to the objects
            would be shaded accordingly to these lights.
            
            There are several types of lights:
                Directional lights, Aerial lights, Spot lights,
                Ambient lights, Point lights.
            
            Also there are another indirect light that will be computed
            in real-time or render time that will depend on the environment.
            Ths light will be specular lights or bouncing lights.

            Finally, effects like Fresnel, bump, dissplacement, sub-surface
            scattering, reflection, refraction, translucency, layers, etc..
            are a cmobination between Materials and lights

    Volumes (VDB): The type of geoemtry is different from the way
            that polygons are created. This type of geometry
            requires additional manipulation and pipelone.

    Particles/Instances: This is used to represent millions of 
            GEoemtry that will be packed into points. So the 
            vertices, and indices will be instances.

    Sprites: Sprites is used for 2D and 3D. The idea is sprites
            will alway be facing to the camera. So there is no
            distorsion or perspective transformation that affect
            to this objects.
    
    Image: Image class will be used to create Interface controls,
            dashboard elements, etc.. 
    

"""

"""
 The new pipeline used for OpenGL is that all operations, transformations,
 etc.. will be performed in the GPU. In order to do this these operations
 must be implemented into the shaders programs instead, so the GPU will be
 able to compile those shaders and execute them in Parallel.

 OpenGL works using states, so for eac state we configure the buffers, arrays,
 shaders, etc.. and finally draw. We perform the sema operation for all the 
 geoemtry we have. Since the geometry could have different configuration 
 and attributes, and shaders we need to operate with them separately.

 When the entire scene is complete, and all the geoemtry all correctly renderer
 it's time to flip the buffers to start the next frame.


"""

class DisplayMode:
    fullscreen  = pygame.FULLSCREEN	# window is fullscreen
    resizable   = pygame.RESIZABLE  # window is resizeable
    noframe     = pygame.NOFRAME	# window has no border or controls
    doublebuf   = pygame.DOUBLEBUF	# use double buffer - recommended for HWSURFACE or OPENGL
    hwaccel     = pygame.HWSURFACE  # window is hardware accelerated, only possible in combination with FULLSCREEN
    opengl      = pygame.OPENGL     # window is renderable by OpenGL

class Display:
    """
        This Class will manager the Display to interact with
        openGL. It will use OpenGL and a double buffer so
        it can sweep between the buffers per frame.

        Also the display is going to manage the interaction
        with the user regarding the events, mouse buttons and
        keypress done.
    """
    
    # Default Display Mode that will be used when crating the window
    # Open GL and Double Buffer are neccesary to display OpenGL
    defaultmode = DisplayMode.opengl|DisplayMode.doublebuf

    # Default Background Color
    defaulBGColor = [0.0, 0.0, 0.0, 1.0]

    def __init__(self, title, width=800, height=600, bpp=16, displaymode = DisplayMode.resizable):
        # Initialize all the variables
        self.title = title
        self.width = width
        self.height = height
        self.bpp = bpp # RGBA 8*8*8*8 = 32 bits per pixel
        self.displaymode = displaymode
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the variables and Memory
        self._dispose()

    def _dispose(self):
        try:
            #Finalize pygame
            pygame.quit()
            # SEt is closed to true
            self.isClosed = True
        except:
            print("ERROR: Error disposing the display.")

    def _initialize(self):
        # dispose and close all the windows prior to initialize
        self._dispose()
        # Initialize and open the display window
        try:
            # Initialize pygame
            pygame.init()
            # Set title bar caption
            pygame.display.set_caption(self.title)
            # Initialize the display
            screen = pygame.display.set_mode((self.width, self.height), 
                                        Display.defaultmode|self.displaymode,
                                        self.bpp)
            # Enable Depth test to avoid overlaped areas
            GL.glEnable(GL.GL_DEPTH_TEST)
            # Clear the image
            self.clear()
            # Set isclosed to false
            self.isClosed = False
        except:
            print("ERROR: Error creating the display.")
   
    def close(self):
        # Set close to true
        self.isClosed = True

    def clear(self, color = defaulBGColor):
        # Clear will clean the windows color.
        GL.glClearColor(*color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def update(self):
        # With depth buffer flip is the way to update screen
        pygame.display.flip()
        # Check to close the window after update the window
        if self.isClosed:
            self._dispose()


class DrawMode:
    triangles    = GL.GL_TRIANGLES	
    points       = GL.GL_POINTS
    lines        = GL.GL_LINES 
    quads        = GL.GL_QUADS
    tfan         = GL.GL_TRIANGLE_FAN
    lstrip       = GL.GL_LINE_STRIP
    tstrip       = GL.GL_TRIANGLE_STRIP

class UsageMode:
    stream_draw  = GL.GL_STREAM_DRAW
    stream_read  = GL.GL_STREAM_READ
    stream_copy  = GL.GL_STREAM_COPY
    static_draw  = GL.GL_STATIC_DRAW
    static_read  = GL.GL_STATIC_READ
    static_copy  = GL.GL_STATIC_COPY
    dynamic_draw = GL.GL_DYNAMIC_DRAW
    dynamic_read = GL.GL_DYNAMIC_READ
    dynamic_copy = GL.GL_DYNAMIC_COPY 

class Geometry:
    """
        This element will create and store all the elements needed
        to Render a Geometrt
    """

    # Declare the subindex that will be used for multiple (vector) attribites
    index_cols = ["x","y","z","w"]

    def __init__(self, name=None, shader=None, mode=DrawMode.triangles, usage=UsageMode.static_draw):
        # Initialize all the variables
        self.name = name
        self.mode = mode
        self.shader = shader
        self.usage = usage
        # Attributes dictionary to store the columns for each component
        self._pointAttribCols = {}
        self._primAttribCols = {}
        # Point Attributes and elements Data frames
        self._dfpoints = pd.DataFrame()
        self._dfPrims = pd.DataFrame()
        # Vertex Array Object for all the Attributtes, elements, etc.
        self._VAO = None
        # Vertex Arrays Buffers for all the Attributes
        self._VAB = {}
        # Vertex Element Buffers for all the Attrbiutes
        self._VEB = None

        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        # Dispose all the object and memory allocated
        GL.glDeleteVertexArrays(1,self._VAO)

    def _copy_to_buffer(self, dfPoints, dfPrims=None):
        # Create a new VAO (Vertex Array Object). Only (1) VAO.
        # Note. Using bpp > 16bits doesn't work. This depend on the Graphic Card.
        self._VAO = GL.glGenVertexArrays(1)
        # Every time we want to use VAO we just have to bind it
        GL.glBindVertexArray(self._VAO)
        # Get the current vertices (flatten)
        vertices = dfPoints[self._pointAttribCols["P"]].values
        # Create the vertex array buffer and send the positions into the GPU buffers
        self._VAB["P"] = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._VAB["P"] )
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices.flatten() , self.usage)
        
        # Bind the shaders attributes for the current geometry
        if self.shader:
            # The first attribute OpenGL search for is for 0 or "position"
            self.shader.bind("position",len(vertices[0]),GL.GL_FLOAT)

        # Unbind VAO from OpenGL. Set to None = 0
        GL.glBindVertexArray(0)
        # Remove and unbind buffers
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        # Unbin shader
        self.shader.bind("position",bind=False)

    def _initialize(self):
        pass

    def update(self):
        # Depenging on the method to update the vertices using GPU or 
        # inmediate OpenGL the update will be different.
        self._copy_to_buffer(self._dfpoints)
    
    def _createAttribute(self, df, name, size=3, values=None, default=None, dtype=np.float32):
        # Check any values or default values has been provided
        if empty(values) and empty(default):
            if df.empty:
                # If nothing to add exit the function
                return None
            else:
                # Create a default value (float)
                default = np.zeros((size), dtype=dtype)
        # Check the index value depending on the size
        if size > 1:
            columns = [name + Geometry.index_cols[i] for i in range(size)]
        else:
            columns = [name]
        # Check if values has been already defined
        if (empty(values) and not df.empty):
            # create an array with the same number of rows as the current
            values = np.tile(default,(len(df.index)))
        # Reshape the values
        values = np.reshape(values, (-1, size))
        # Check if the DataFrame is empty
        if df.empty:
            # Add the current data into the attributes frame
            df = pd.DataFrame(values, columns=columns)
        else:
            # Add the current data into the attributes frame
            dfvalues = pd.DataFrame(values, columns=columns)
            # Append both dataframes
            df = pd.merge(df, dfvalues, how='inner', left_index=True, right_index=True)
        # Set the columns into the the current Point attribute
        return (df, columns)

    def getPrimsAttrib(self, name):
            return self._dfPrims[self._primAttribCols[name]]

    def delPrimsAttrib(self, name):
        self._dfPrims.drop(self._primAttribCols[name], axis=1, inplace=True)

    def addPrimsAttrib(self, name, size=3, values=None, default=None, dtype=np.float32):
        # Get the new attribute and dataframe
        result = self._createAttribute(self._dfPrims,name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self._dfPrims = result[0]
            # Set the columns into the the current Point attribute
            self._primAttribCols[name] = result[1]

    def addIndices(self, values, size=3,):
         #Add prims Attributes Elements
        self.addPrimsAttrib("Id",size,values)
   
    def getPointAttrib(self, name):
        return self._dfpoints[self._pointAttribCols[name]]

    def delPointAttrib(self, name):
        self._dfpoints.drop(self._pointAttribCols[name], axis=1, inplace=True)

    def addPointAttrib(self, name, size=3, values=None, default=None, dtype=np.float32):
        # Get the new attribute and dataframe
        result = self._createAttribute(self._dfpoints,name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self._dfpoints = result[0]
            # Set the columns into the the current Point attribute
            self._pointAttribCols[name] = result[1]

    def addPoints(self, values, size=3):
        #Add point Attributes Position
        self.addPointAttrib("P",size,values)

    def addNormals(self, normals, size=3):
          #Add point Attributes Normals
        self.addPointAttrib("N",size,normals)

    def render(self):
        # Use the current Shader configuration
        self.shader.use()
        # Bind the created Vertex Array Object
        GL.glBindVertexArray(self._VAO)
        # Draw the current geoemtry. Check if indices have been added
        if "id" in self._primAttribCols:
            GL.glDrawElements(self.mode, len(self._dfpoints.index), 
                              GL.GL_UNSIGNED_INT, self.getPrimstAttrib("Id").values)
        else:
            GL.glDrawArrays(self.mode, 0, len(self._dfpoints.index))
        # Unbind VAO from GPU
        GL.glBindVertexArray( 0 )
        # Set no use the current shader configuration
        self.shader.use(False)
  
ShaderType = {
    "VERTEX_SHADER"     : { "id":"vs", "type":GL.GL_VERTEX_SHADER   }, 
    "FRAGMENT_SHADER"   : { "id":"fs", "type":GL.GL_FRAGMENT_SHADER },
    "GEOMETRY_SHADER"   : { "id":"gs", "type":GL.GL_GEOMETRY_SHADER }
    }

class Shader:
    """
        This element will create and store all the elements needed
        to create a shader.
    """
    
    def __init__(self, name=None, filepath="./"):
        # Initialize all the variables
        self.name = name
        self.filepath = filepath
        # Initial variables
        self._shaders = {}
        self._attributes = {}
        self._uniforms = {}
        self._program = None
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        # Dispose all the object and memory allocated
        for key,value in self._shaders.items():
            if self._program:
                GL.glDetachShader(self._program, value)
            GL.glDeleleShader(value)
        # DeleteShader Program
        if self._program:
            GL.glDeleteProgram(self._program)

    def _initialize(self):
        # Dispose previous elemens created
        self._dispose()
        # Create the variables needed for the shader program
        self._shaders = {}
        self._attributes = {}
        self._uniforms = {}
        self._program = GL.glCreateProgram()
        # Read all shader files and link into the progrma
        for key,value in ShaderType.items():
            filename = self.filepath + "/" + self.name + "." + value["id"]
            shader = self._load_shader(self._program, filename, value["type"])
            # Check the current shader has been loaded correctly
            if shader:
                self._shaders[key] = shader
        # Link the current shader program
        GL.glLinkProgram(self._program)
        # Check for link errors                
        if self._check_shader_error(self._program, GL.GL_LINK_STATUS,True):    # Check if compilation was successful
            return
        # Validate Program
        GL.glValidateProgram(self._program)
         # Check for link errors                
        if self._check_shader_error(self._program, GL.GL_VALIDATE_STATUS,True):    # Check if compilation was successful
            return

    def _check_shader_error(self,shader,status,isProgram=False):
        if isProgram:
            # Check for errors in Programs               
            if GL.glGetProgramiv(shader,status) != GL.GL_TRUE:
                print('Program load failed: {}'.format(GL.glGetProgramInfoLog(shader)))
                return True
        else:
            # Check for errors in Shaders                
            if GL.glGetShaderiv(shader,status) != GL.GL_TRUE:
                print('Shader load failed: {}'.format(GL.glGetShaderInfoLog(shader)))
                return True
        return False    

    def _load_shader(self, program, filename, shader_type):
        # Check if the file exists
        if isfile(filename):
            #Load current shader code-source from file
            shader_source = readfile(filename)
            # Create curent shader
            current_shader = GL.glCreateShader(shader_type)
            # Set the source for the current sshader
            GL.glShaderSource(current_shader, shader_source) 
            # Compile current shadershader
            GL.glCompileShader(current_shader)
            # Check for compiler errors                
            if self._check_shader_error(current_shader, GL.GL_COMPILE_STATUS):    # Check if compilation was successful
                return None
            # Finally attach the current shader to the program
            GL.glAttachShader(program, current_shader)
            # Return the current shader
            return current_shader

    def load(self, filename):
        #Set the current file and initialize
        self._filename = filename
        self._initialize()

    def use(self,use=True):
        if self._program:
            # Tell Open GL to use/not-use the current progrma
            if use:
                GL.glUseProgram(self._program)
            else:
                GL.glUseProgram(0)

    def bind(self,name,size=3,gltype=GL.GL_FLOAT, bind=True):
        if self._program is None:
            return False
        if bind:
            # Get the location of the 'name' in parameter of our shader and bind it.
            attribute = GL.glGetAttribLocation(self._program, name)
            GL.glEnableVertexAttribArray(attribute)
            # Describe the position data layout in the buffer
            GL.glVertexAttribPointer(attribute,size,gltype,False, 0, ctypes.c_void_p(0))
            # Insert current attribite binding
            self._attributes[name] = attribute
        else:
            # Unbind Attribute
            GL.glDisableVertexAttribArray(self._attributes[name])
   
    def update(self):
        pass

# Testing pourposes main function
if __name__ == "__main__":
    with  Display("Main Window", 800,600) as display:

        shader = Shader("default_shader", "./shaders")
        # shader.use()

        vertices = [ 0.6,  0.6, 0.0, 1.0,
                    -0.6,  0.6, 0.0, 1.0,
                     0.0, -0.6, 0.0, 1.0]
        # Create the geometry
        cube = cube3D()
        myCube = Geometry("Cube#1",shader)
        myCube.addPoints(vertices, 4)
        myCube.update()
        # myCube.addIndices(cube[1])
        # myCube.addNormals(cube[0], 4)

        # myCube.addPointAttrib("Up", size=4, values=cube[0])
        # myCube.addPointAttrib("pscale", size=3, default=[0.4,0.4,0.4])

        # myCube.update()
        # print(myCube.getPointAttrib("P").head())
        # #print(myCube.primitives["Idx"].head())
        # print(myCube.getPointAttrib("N").head())
        # print(myCube.getPointAttrib("pscale").pscalez.head())
        # print(myCube.getPointAttrib("pscale").values)
        # myCube.delPointAttrib("pscale")

        # print(myCube._dfpoints.head())


        while not display.isClosed:     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.close()
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    display.close()
            # Clear the display
            display.clear()
            # Render the  geometry
            myCube.render()
            # Update the display
            display.update()

