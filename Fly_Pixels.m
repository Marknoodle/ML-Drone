


mycam = webcam('j5 WebCam JVCU100'); %%% The argument is the usb camera in the research room: 'j5 WebCam JVCU100'
preview(mycam)


flyToPoint = [640,360];

[bwImg,Ydrone,Xdrone] = GreenPosition(mycam);


pixelDistance = pdist([flyToPoint;Xdrone,Ydrone] ,'euclidean'); %1 meter is about 295 pixels
[Angle,Radian]=getAngle([Xdrone,Ydrone],flyToPoint);


flyDistance = pixelDistance * (1/295); %calculate actual flight distance

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When drone is facing monitor
trueAngle = deg2rad(-1 *(Angle - 180));  
%Q1 %% Q2

%trueAngle = deg2rad(180 - Angle);  
%Q4 && Q3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% LIGHTS ON
r = ryze();%Connect to Drone and Make Drone Obj

speed = .5; %Meters/Sec
takeoff(r);

if abs(trueAngle) > deg2rad(5) 
turn(r,trueAngle);
end

moveforward(r, 'Distance', flyDistance, 'Speed', speed, 'WaitUntilDone', true);

land(r);














function [bwImg,XgreenCentre,YgreenCenter] = GreenPosition(mycam)

tim = tic;
duration = 2;
greenThreshold = 25;  %The "Green-ness" level
while(toc(tim) < duration)

img = snapshot(mycam);

    
%% Extract RGB color components from the FPV camera image
r = img(:,:,1);
g = img(:,:,2);
b = img(:,:,3);

%% Calculate the number of rows and coloumns in the FPV camera image
nRows = size(img, 1);
nCols = size(img, 2);

%% Approximate the intensity of green components in the image
greenIntensities = g - r/2 - b/2; % How green is your green?

%% Threshold the image to find the regions that we consider to be green enough
bwImg = greenIntensities > greenThreshold;

% Find indices of green pixels in the image
[row, col] = find(bwImg); %Where is the green? 

    
    % Find green pixels and track the ball using drone if there are enough
    % green pixels in the image

    % Find center of the green ball in the captured image
    if ~isempty(row) && ~isempty(col)
        XgreenCentre = round(mean(row));
        YgreenCenter = round(mean(col));
        
%         if toc(tim) > 5  %Take a lookie at bwImg and playwith it with respect to green center (X,Y)
%             a = 2;
%         end
        
        imshow(bwImg)
    end



pause(0.1);
end

end



%% Used to measure how far we should turn to fly to point
%% Borrowed from https://www.mathworks.com/matlabcentral/fileexchange/60148-get-angle-and-radian-between-two-points

function [Angle,Radian]=getAngle(point_O,point_P)
%Input O-(x1,y1) and P(x2,y2)points
%Output Angle And Radian
%devloper Er.Abbas Manthiri S
%Email-abbasmanthiribe@gmail.com
%Angle get accurate if line length is high
if nargin~=2
    [row_O,col_O]=size(point_O);
    if row_O==4
        point_P= point_O(3:4,:);
        point_O= point_O(1:2,:);
    elseif col_O==4
        point_P= point_O(:,3:4);
        point_O= point_O(1:1:2);
    else
        error('Input Type is Wrong')
    end
end
if ~(isnumeric(point_O) && isnumeric(point_P))
    error('Inputs Must be numeric value')
end
[row_O,col_O]=size(point_O);
[row_P,col_P]=size(point_P);
if ~(isvector(point_O) && isvector(point_P))
    if row_O~=row_P && col_O==col_P && col_O==2
        if row_O>row_P && row_P==1
            point_P=repmat(point_P,row_O,1);
        elseif row_O<row_P && row_O==1
            point_O=repmat(point_O,row_P,1);
        else
            error('Matrix Dimention must agree')
        end
    elseif col_O~=col_P && row_O==row_P && row_O==2
        if col_O>col_P && col_P==1
            point_P=repmat(point_P',col_O,1);
        elseif col_O<col_P && col_O==1
            point_O=repmat(point_O',col_P,1);
        else
            error('Matrix Dimention must agree')
        end
    else
        error('Input format is wrong')
    end
else
    if length(point_O)==length(point_P)
        point_O=transpose(point_O(:));
        point_P=transpose(point_P(:));
    else
        error('Input must be same size')
    end
end
X=point_P(:,1)-point_O(:,1);
Y=point_P(:,2)-point_O(:,2);
Z=sqrt(X.^2+Y.^2);
Angle=zeros(size(Z));
Amax=360;
X1=point_O(:,1);
X2=point_P(:,1);
Y1=point_O(:,2);
Y2=point_P(:,2);
X=X2-X1;
Y=Y2-Y1;
X=X./Z;
Y=Y./Z;
Angle(sign(Y2)>0)=acosd(X(sign(Y2)>0));
Angle(sign(Y2)<0  & sign(X2)>0)=Amax+asind(Y(sign(Y2)<0  & sign(X2)>0));
Angle(~(sign(Y2)>0  | (sign(Y2)<0  & sign(X2)>0)))=Amax-acosd(X(~(sign(Y2)>0  | (sign(Y2)<0  & sign(X2)>0))));
Angle(Angle==Amax)=0;
Radian=Angle*pi/180;
end