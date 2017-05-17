#version 330

in vec4 position;
in vec4 Cd;
in vec2 UV;

out vec4 oCd;
out vec2 oUV;

void main()
{
   gl_Position = position;
   oCd = Cd;
   oUV = UV;
}
