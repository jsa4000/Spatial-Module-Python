#version 330

in vec4 oCd;
in vec2 oUV;

uniform sampler2D diffuse;

void main()
{
   gl_FragColor = texture2D(diffuse,oUV);
}