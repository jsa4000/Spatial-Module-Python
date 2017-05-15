
import numpy as np
import OpenGL.GL as GL
import OpenGL.GL.shaders
import pygame
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
        1.0, -1.0, -1.0, 1.0, # right, bottom, front vertex. (0)
        -1.0, -1.0, -1.0, 1.0, # left, bottom, front vertex. (1)
        -1.0, -1.0, 1.0, 1.0, # right, bottom, back vertex. (2)
        1.0, -1.0, 1.0, 1.0, # left, bottom, back vertex. (3)
        # The same vertex positions but on the top of the cube Y= 1
        1.0, 1.0, -1.0, 1.0, # right, bottom, front vertex. (0)
        -1.0, 1.0, -1.0, 1.0, # left, bottom, front vertex. (1)
        -1.0, 1.0, 1.0, 1.0, # right, bottom, back vertex. (2)
        1.0, 1.0, 1.0, 1.0 # left, bottom, ack vertex. (3)
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


def isEmpty(value):
        if isinstance(value, (list, dict, np.ndarray, tuple, set)):
            if len(value) > 0:
                return False
        else:
            if value is not None:
                return False
        return True

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

    def __init__(self, title, width=800, height=600, bpp=32, displaymode = DisplayMode.resizable):
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

class Geometry:
    """
        This element will create and store all the elements needed
        to Render a Geometrt
    """

    # Declare the subindex that will be used for multiple (vector) attribites
    index = ["x","y","z","w"]

    def __init__(self, name = None):
        # Initialize all the variables
        self.name = name
        # Attributes group
        self.points = {}
        self.primitives = {}
        # Attributes and elements Data frames
        self._dfpoints = pd.DataFrame()
        self._dfprimitives = pd.DataFrame()
        # Vertex Array Object for all the Attributtes, elements, etc.
        self._VAO = None
        # Vertex Arrays Buffers for all the Attributes
        self._VAB = []
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
        # Dispose all the object and vmemry allocated
        pass

    def _initialize(self):
        pass

    def addPrimitives(self, indices):
        # In OpenGL a face will be defined by using 3 vertices (triangles)
        indexes = ["id0","id1","id2"]
        # Reshape the current array into 3 columns
        indices = np.reshape(indices, (-1, len(indexes)))
        self._dfprimitives = pd.DataFrame(indices,columns=indexes)
        # Group the current Primitive attribute
        self.primitives["Idx"] = self._dfprimitives.groupby(indexes)

    def addPointAttribute(self, name, size=3, values=None, default=None, dtype = np.float32):
        # Check any values or default values has been provided
        if isEmpty(values) and isEmpty(default):
            if self._dfpoints.empty:
                # If nothing to add exit the function
                return
            else:
                # Create a default value (float)
                default = np.zeros((size), dtype=dtype)
             
        # Check the index value depending on the size
        if size > 1:
            columns = [name + Geometry.index[i] for i in range(size)]
        else:
            columns = [name]

        # Check if values has been already defined
        if (isEmpty(values) and not self._dfpoints.empty):
            # create an array with the same number of rows as the current
            values = np.tile(default,(len(self._dfpoints.index)))

        # Reshape the values
        values = np.reshape(values, (-1, size))

        #Create the indexes
        index = np.arange(len(self._dfpoints.index),dtype=np.int32)

        if self._dfpoints.empty:
            # Add the current data into the attributes frame
            self._dfpoints = pd.DataFrame(values, index=index, columns=columns)
        else:
             # Add the current data into the attributes frame
            dfvalues = pd.DataFrame(values, index=index,columns=columns)
            # Append both dataframes
            self._dfpoints = pd.merge(self._dfpoints, dfvalues, how='inner', left_index=True, right_index=True)
         # Group the current Point attribute
        self.points[name] = self._dfpoints.groupby(columns, sort=False)
        # Print the result
        print(self.points[name].head())


    def addPoints(self, vertices, size=3):
        # Get the number of dimension for the points
        indexes = ["P" + Geometry.index[i] for i in range(size)]
        vertices = np.reshape(vertices, (-1, size))
        # Add the current data into the attributes frame
        self._dfpoints = pd.DataFrame(vertices, columns=indexes)
        # Group the current Point attribute
        self.points["P"] = self._dfpoints.groupby(indexes)

    def addNormals(self, normals, size=3):
        # Get the number of dimension for the points
        indexes = ["N" + Geometry.index[i] for i in range(size)]
        normals = np.reshape(normals, (-1, size))
        # Add the current data into the attributes frame
        dfnormals = pd.DataFrame(normals, columns=indexes)
        # Append both dataframes
        self._dfpoints = pd.merge(self._dfpoints, dfnormals, how='inner', left_index=True, right_index=True)
        # Group the current Point attribute
        self.points["N"] = self._dfpoints.groupby(indexes)

    def render(self):
        pass
  
# Testing pourposes main function
if __name__ == "__main__":
    with  Display("Main Window", 800,600) as display:

        # Create the geometry
        cube = cube3D()
        myCube = Geometry("Cube#1")
        # myCube.addPoints(cube[0], 4)
        # myCube.addPrimitives(cube[1])
        # myCube.addNormals(cube[0], 4)

        myCube.addPoints(cube[0], 4)
        myCube.addPointAttribute("N", size=4, values=cube[0])
        myCube.addPointAttribute("pscale", size=1, default=0.0)

        print(myCube.points["P"].head())
        #print(myCube.primitives["Idx"].head())
        print(myCube.points["N"].head())
        print(myCube.points["pscale"].head())

        while not display.isClosed:     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.close()
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    display.close()
            # Clear the display
            display.clear()
            # Update the display
            display.update()

