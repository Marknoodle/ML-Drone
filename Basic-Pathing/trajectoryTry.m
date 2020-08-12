g = 9.81;
t=2.5; %in seconds
Vox=2;
Voy=8.25;
tx=0:.1:2.5; %this will give me an array for the time of the diver in the x position
ty=0:.1:2.5; %this will give the array for the time of the diver in the y-position

[tx,ty] = trajectory(Vox,Voy,tx,ty,g);

function [tx,ty]= trajectory(Vox,Voy,tx,ty,g)%function for varying angle
x=Vox*cos(0)*tx; %gives the position of the x
y=Voy*(sin(0)*ty)-(.5*g*(ty.^2)); %gives the position of the y
plot (x,y)
end
