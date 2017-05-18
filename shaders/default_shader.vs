#version 330

in vec4 position;
in vec4 Cd;
in vec2 UV;

uniform mat4 world_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

out vec4 oCd;
out vec2 oUV;

void main()
{
   gl_Position = projection_matrix * view_matrix * world_matrix * position;
   oCd = Cd;
   oUV = UV;
}
