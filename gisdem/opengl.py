
import OpenGL.GL as GL
import OpenGL.GL.shaders
import ctypes
import pygame
import os
from PIL import Image
import numpy as np
import pandas as pd


# Great useful resource to learn OpenGL and all the concepts needed for understanding
# ligths, materials, shaders, transformations, etc..
# URL: https://learnopengl.com/, https://open.gl/drawing

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

def Rectangle3D():
    vertices = [
        -0.5, -0.5, 0.0, 1.0,
         0.5, -0.5, 0.0, 1.0,
         0.5,  0.5, 0.0, 1.0,
        -0.5,  0.5, 0.0, 1.0
           ]
    indices = [
        0, 1, 2, 
        2, 3, 0
    ]
    return (np.asarray(vertices, dtype=np.float32),np.asarray(indices, dtype=np.uint32))

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
        -0.5, -0.5, 0.5, 1.0, # right, bottom, back vertex. (0)
         0.5, -0.5, 0.5, 1.0, # left, bottom, back vertex. (1)
         0.5,  0.5, 0.5, 1.0, # left, bottom, ack vertex. (2)
        -0.5,  0.5, 0.5, 1.0, # right, bottom, back vertex. (3)   
        # The same vertex positions but on the top of the cube Y= 1
        -0.5, -0.5, -0.5, 1.0, # left, bottom, front vertex. (4)
         0.5, -0.5, -0.5, 1.0, # right, bottom, front vertex. (5)
         0.5,  0.5, -0.5, 1.0, # right, bottom, front vertex. (6)
        -0.5,  0.5, -0.5, 1.0 # left, bottom, front vertex. (7)
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
        0, 1, 2, 2, 3, 0, # Bottom face
        4, 5, 6, 6, 7, 4, # Front face
        4, 5, 1, 1, 0, 4, # left side
        6, 7, 3, 3, 2, 6, # back face
        5, 6, 2, 2, 1, 5, # Right Side
        7, 4, 0, 0, 3, 7 # Top face
     ]
    #Conver the array into a numpy array (copy vs reference)
    nindices = np.asarray(indices, dtype=np.uint32)
    # The vertices are not repeated. You can have the vertices repeated if
    # you need different attrbiutes for them, like the normals, This will
    # be used to shade the elements in different ways. In some programs
    # This is called vertex normals. An it's used to crease or decrease
    # the weight for the transition between face to face. It's like define
    # smooth areas between the hard-surface areas.
    
    # It will return a tuple with the vertices and indices.
    #return (nvertices,nindices)
    return (vertices,indices)

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

def typeGL(dtype):
    """
        This function will convert the types supported by OpenGL from
        numpy types. 
        If dtype is not founded into the GLtypes the function will
        return GL.GL_FLOAT as default Open GL type
    """
    # Check for some posibilities with the input, np.int32, 'int32','np.int32'
    if isinstance(dtype, (np.dtype)):
        dtype = dtype.name
    elif not isinstance(dtype, (str)):
        dtype = dtype.__name__
    # get the second part in case it can be splitted
    if len(dtype.split(".")) > 1:
        dtype = dtype.split(".")[-1]
    #Check the type of data has to be converted
    datatypes = {
        "int8"     :    GL.GL_BYTE, 			
        "uint8"    :    GL.GL_UNSIGNED_BYTE,	
	    "int16"    :    GL.GL_SHORT,			
	    "uint16"   :    GL.GL_UNSIGNED_SHORT,	
	    "int32"    :    GL.GL_INT,				
	    "uint32"   :    GL.GL_UNSIGNED_INT,		
	    "float16"  :    GL.GL_HALF_FLOAT,		
	    "float32"  :    GL.GL_FLOAT,			
	    "float64"  :    GL.GL_DOUBLE,
        "fixed"    :    GL.GL_FIXED # More compatibility for OS (float32)
    }	
    # Check if the current datatype exists
    if dtype in datatypes:		
        return datatypes[dtype]
    # if the data type does't exit returns default GL type
    return datatypes[np.float32]

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
    #Defaule type that will be used for indexing using OpenGL elements array buffer
    index_type = np.uint32

    def __init__(self, name=None, shader=None, mode=DrawMode.triangles, usage=UsageMode.static_draw):
        # Initialize all the variables
        self.name = name
        self.shader = shader
        self.mode = mode
        self.usage = usage
        # Attributes dictionary to store the columns for each component
        self._pointAttribCols = {}
        self._primAttribCols = {}
        # Point Attributes and elements Data frames
        self._dfPoints = pd.DataFrame()
        self._dfPrims = pd.DataFrame()
        # Vertex Array Object for all the Attributtes, elements, etc.
        self._VAO = None
        # Vertex Arrays Buffers for all the Attributes
        self._VAB = {}
        # Element Array Buffers for all the Attrbiutes
        self._EAB = None

        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        # Dispose all the objects and memory allocated
        GL.glDeleteVertexArrays(1,self._VAO)

    def _has_indices(self):
        if "Id" in self._primAttribCols:
            return True
        return False

    def _create_vertex_buffer_array(self, name, attribute_name = None):
        """
            This function only make sense to do when working with
            points (vertex) attributes.S
            The function  will return the bind attribute attached
            to the shader. This could be stored into a list to 
            detach later when copy all the buffers and after unbind
            VAO object.
        """
        # Check if not attribute name has been mapped for the bidinng
        if attribute_name is None:
            attribute_name = name
        # Get the current vertices (flatten is not needed)
        vertices = self._dfPoints[self._pointAttribCols[name]].values
        # Create the vertex array buffer and send the positions into the GPU buffers
        self._VAB[name] = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._VAB[name] )
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, self.usage)

        # Bind Attribute to the current shader. 
        return self.shader.bind(attribute_name, len(vertices[0]), vertices.dtype)

    def _copy_to_buffer(self):
        # Bind the shaders attributes for the current geometry
        if self.shader is None:
            print("ERROR: No shader specified")
      
        # Create a list with the attributes created and binded
        shader_attributes = []

        # Create a new VAO (Vertex Array Object). Only (1) VAO.
        #   Note. Using bpp > 16bits doesn't work. This depend on the Graphic Card.
        self._VAO = GL.glGenVertexArrays(1)
        # Every time we want to use VAO we just have to bind it
        GL.glBindVertexArray(self._VAO)

        # Create the first attribute "position" (location = 0) (Mandatory)
        shader_attributes.append(self._create_vertex_buffer_array("P","position"))
        
        # Check wether the geometry has indexes
        if self._has_indices():
            # Get the current indices (flatten)
            indices = self._dfPrims[self._primAttribCols["Id"]].values
            # Create the element array buffer and send the positions into the GPU buffers
            self._EAB = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,  self._EAB);
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, self.usage);
        
        # Create and bind other Attributes
        for attrib in self._pointAttribCols.keys():
            if attrib != "P":
                shader_attributes.append(self._create_vertex_buffer_array(attrib))

        # Unbind VAO from OpenGL. Set to None = 0
        GL.glBindVertexArray(0)
        # Remove and unbind buffers
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        # Unbind all the Attributes "position" + Additionals
        for attribute in shader_attributes:
            self.shader.unbind(attribute)

    def _initialize(self):
        pass
        
    def update(self):
        # Depenging on the method to update the vertices using GPU or 
        # inmediate OpenGL the update will be different.
        self._copy_to_buffer()
    
    def _createAttribute(self, df, name, size=3, values=None, default=None, dtype=None):
        #Check the data type if any
        if dtype is None:
            if empty(values):
                # Assign a default value
                dtype = np.float32
            else:
                # Get the type from the values
                if not isinstance(values,(np.ndarray)):
                    # If not numpy then get the numppy array 
                    values = np.array(values)
                #Finally get the type from the numpy array
                dtype = values.dtype 
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
        # Reshape the values [ Maybe should be normalized and flatten]
        values = np.array(np.reshape(values, (-1, size)) ,dtype=dtype)
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

    def addPrimsAttrib(self, name, values=None, size=3,  default=None, dtype=None):
        # Get the new attribute and dataframe
        result = self._createAttribute(self._dfPrims,name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self._dfPrims = result[0]
            # Set the columns into the the current Point attribute
            self._primAttribCols[name] = result[1]

    def addIndices(self, values, size=3, dtype=np.uint32):
         #Add prims Attributes Elements
        self.addPrimsAttrib("Id", values, size, dtype=dtype)
   
    def getPointAttrib(self, name):
        return self._dfPoints[self._pointAttribCols[name]]

    def delPointAttrib(self, name):
        self._dfPoints.drop(self._pointAttribCols[name], axis=1, inplace=True)

    def addPointAttrib(self, name, values=None, size=3,  default=None, dtype=None):
        # Get the new attribute and dataframe
        result = self._createAttribute(self._dfPoints,name,size,values,default,dtype)
        if not empty(result):
            # Set the returned dataframe with the new attribute
            self._dfPoints = result[0]
            # Set the columns into the the current Point attribute
            self._pointAttribCols[name] = result[1]

    def addPoints(self, values, size=3, dtype=np.float32):
        #Add point Attributes Position
        self.addPointAttrib("P", values, size, dtype)

    def addNormals(self, values, size=3, dtype=np.float32):
          #Add point Attributes Normals
        self.addPointAttrib("N", values, size, dtype)

    def render(self):
        # Bind the created Vertex Array Object
        GL.glBindVertexArray(self._VAO)
        # Draw the current geoemtry. Check if indices have been added
        if self._has_indices():
            GL.glDrawElements(self.mode, len(self._dfPrims.index) * 3, 
                              typeGL(Geometry.index_type), ctypes.c_void_p(0))
        else:
            GL.glDrawArrays(self.mode, 0, len(self._dfPoints.index))
        # Unbind VAO from GPU
        GL.glBindVertexArray(0)
  
# Shader typas allow and extension for the files to use
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
        self._uniforms = {}
        self._program = None
        # variable to tell if the shader has been initialized correctly
        self.initialized = False
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
        for shader in self._shaders:
            GL.glDetachShader(self._program, self._shaders[shader])
            GL.glDeleleShader(self._shaders[shader])
        # Delete Shader Program
        if self._program:
            GL.glDeleteProgram(self._program)
        # Set initialized to false
        self.initialized = False

    def _initialize(self):
        # Dispose previous elemens created
        self._dispose()
        # Create the variables needed for the shader program
        self._shaders = {}
        self._uniforms = {}
        # Set initialized to false
        self.initialized = False
        # Create the main shader program
        self._program = GL.glCreateProgram()
        # Generate the main path for the shaders to load
        filename = self.filepath + "/" + self.name + "."
        # Read all shader type files and link into the progrma
        for key,value in ShaderType.items():
            shader = self._load_shader(filename + value["id"], value["type"])
            # Check the current shader has been loaded correctly
            if shader:
                # Finally attach the current shader into the program
                GL.glAttachShader(self._program, shader)
                # Add current shader
                self._shaders[key] = shader
        # Link the current shader program
        GL.glLinkProgram(self._program)
        # Check for link errors                
        if self._check_shader_error(self._program, GL.GL_LINK_STATUS,True):    
            return
        # Validate Program
        GL.glValidateProgram(self._program)
         # Check for link errors                
        if self._check_shader_error(self._program, GL.GL_VALIDATE_STATUS,True):
            return
        # if all ok then set initialized to true
        self.initialized = True

    def _load_shader(self, filename, shader_type):
        # Check if the file exists
        if isfile(filename):
            #Load current shader code-source from file
            shader_source = readfile(filename)
            # Create curent shader
            shader = GL.glCreateShader(shader_type)
            # Set the source for the current sshader
            GL.glShaderSource(shader, shader_source) 
            # Compile current shadershader
            GL.glCompileShader(shader)
            # Check for compiler errors                
            if self._check_shader_error(shader, GL.GL_COMPILE_STATUS):
                return None
            # Return the current shader
            return shader
        #Return None if no file exists
        return None

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

    def load(self, name):
        # Set the current file and initialize
        self.name = name
        # Call to initialize so it will load again the program and shader
        self._initialize()

    def use(self,use=True):
        """
            Function to tell Open GL to use this Shader program.
            If the shader won't be used anymore then use use=False.
        """
        if self.initialized:
            # Tell Open GL to use/not-use the current progrma
            if use:
                GL.glUseProgram(self._program)
            else:
                GL.glUseProgram(0)
            return True
        # Not initialized
        return False

    def bind(self, attribute_name, size, dtype=np.float32):
        """
            This function will allow to bind attributes from the array buffer object
            to the shader. This operation will be done per VAO since it can store this
            binding. Again when a VAO will be opened and binding to OpenGL, this
            will bind again all the bindings previously performed during the creation.

            After unbind the current VAO and after loading all the buffers needed
            is very convenient to unbind the attribute after.

            Parameters:
                attribute_name (str): 
                    name of the attribute to use into the shader source-code.
                size:
                    size of the current attribute. This is the number of elements, not
                    de number of bytes etc.. ej. vector3 will have size = 3
                dtype:
                    data-type of the values for the given attribute. If the vector contains
                    int, float32, unit32, etc.. This must be given using GL types. Use
                    typeGL function to convert numpy types into OpenGL types

        """
        if self.initialized:
            # Get the location of the 'attribute_name' in parameter of our shader and bind it.
            attribute_id = GL.glGetAttribLocation(self._program, attribute_name)
            # Check if the current attribute is in the Shader
            if attribute_id != -1:
                #Enable current attribute in the shader
                GL.glEnableVertexAttribArray(attribute_id)
                # Describe the attribute data layout in the buffer
                GL.glVertexAttribPointer(attribute_id, size, typeGL(dtype),
                                    False, 0, ctypes.c_void_p(0))
                # Return the attribute id
                return attribute_id
            else:
                # Attribute has been discarted for the compiler or doesn't exist.
                print ("Warning: Current attribute {} is not ins the shader".format(attribute_name))
        # Return false is not initialized
        return False

    def unbind(self, attribute_id):
        """
            This operation will be performed after unbind the VAO obhect. The parameter
            needed will be the result of the previous result that the bind function call
            returns with the attribute id.
        """
        if self.initialized:
            # Unbind Attribute
            GL.glDisableVertexAttribArray(attribute_id)
        
    def update(self):
        pass

def load_image(filename, bpp=8):
    # Load the image using the path configured
    image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    if (bpp == 32):
        dtype = np.uint32
    elif (bpp == 16):
        dtype = np.uint16
    else:
        dtype = np.uint8
    # Convert the image to a numpy string. Converto to uint8 image.
    image_data = np.fromstring(image.tobytes(), dtype)
    return [image_data, image.size]

class Texture:
    """
        This class will create and store all the elements needed
        to create the texture.
        The module needed to load the images is Pillow
            from PIL import Image
    """
    # Maximun number of textures
    max_textures = 32

    def __init__(self, filename):
        # Initialize all the variables
        self.filename = filename
        # Create a texture variable with the pointer to the buffer
        self._texture = None
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        pass

    def _initialize(self):
        # Create the texture and copy into OpenGL
        self._texture = self._load_Texture(self.filename)

    def _load_Texture(self,filename):
        # Check if the file exists
        if isfile(filename):
            # Load the image using the path configured
            img_data, size = load_image(filename)
            width, height = size
            # Generate texture buffer to load into GPU
            texture = GL.glGenTextures(1)
            # Set initial parameters needed prior send the image to OpenGL
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
            # Bind current texture buffer to load the data
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
            # Set parameters to tell OpenGL how to draw the image
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0,
                            GL.GL_RGBA, typeGL(img_data.dtype), img_data)
            # Create different Mipmaps for the current texure
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
            return texture
        # If not exist return None
        return None
    
    def bind(self, count):
        """
            This method will bind the current texture to be used to the graphic card
            Parameter:
                count: this is used to assign a free slot to the texture into OpenGL
                    [   Some graphic cards could have a limitation in the number of   ]
                    [   textures that can store, depending on the memory.             ]
        """
        if self._texture and (count > 0 and count < Texture.max_textures + 1 ):
            # Following we will activate the texture in a slot 
            GL.glActiveTexture(GL.GL_TEXTURE0 + count)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)

def Triangle():
     #Create default vertices 4f
    vertices = [ -0.5, -0.5, 0.0, 1.0,
                  0.0,  0.5, 0.0, 1.0,
                  0.5, -0.5, 0.0, 1.0]
    indices = [ 0, 1, 2 ]
    color = [ 1.0, 0.0, 0.0, 1.0,
              0.0, 1.0, 0.0, 1.0,
              0.0, 0.0, 1.0, 1.0]
    uvs = [0.0, 0.0,
           0.5, 1.0,
           1.0, 0.0 ]
    return [vertices, indices, color, uvs]

# Testing pourposes main function
if __name__ == "__main__":
    # Create the Display with the main window
    with  Display("Main Window",800,600) as display:
       
        #georaw = cube3D()
        georaw = Triangle()
        
        #text = Texture("./shaders/texture.png")

        # Create the default shader
        shader = Shader("default_shader", "./shaders")
        # Create the geometry
        geo = Geometry("geo",shader)
        #geo.addPoints(georaw[0], 4)
        geo.addPointAttrib("P",georaw[0], 4)
        geo.addIndices(georaw[1])
        geo.addPointAttrib("Cd",georaw[2], 4)
        geo.addPointAttrib("UV",georaw[3], 2)
        #geo.addPoints(vertices, 4)
        geo.update()
         # Start the Main loop for the program
        while not display.isClosed:     
            # Manage the event from the gui
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.close()
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    display.close()
                        
            # Clear the display
            display.clear()
            
            # Render all the elements that share the same shader.
            # Use the current Shader configuration
            shader.use()
            # Render the  geometry
            geo.render()
            # End Use the current Shader configuration
            shader.use(False)

            # Update the display
            display.update()

        # End of the program

