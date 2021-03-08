

%%% CURRENT OBJECTIVE: Place the drone down somewhere and have it... 
%%%                     1) Obtain drone start position ✓
%%%                     2) Obtain angle between drone and fly to point ✓
%%%                     3) Have Drone take off, then turn towards fly to point ✓
%%%                     4) Fly drone to ONE fly to point then land ✓
%%%                     5) Fly drone to several fly to points all in one flight then land 
%%%                     6) Create method to obtain fly to points from shape
%%%                     7) Track drone's flight path in real time using green tracking algorithm and drone height

%LIGHTS OFF
mycam = webcam('j5 WebCam JVCU100'); %%% The argument is the usb camera in the research room: 'j5 WebCam JVCU100'
preview(mycam)


flyToPoint = [493,512]; % Arbitrary Pixel Point (for now). Use "Green Pixel Marking" method to obtain pixel coordinate(s).
%^^^ Next step will be to use a list of several fly to x&y points

% [bwImg,Ydrone,Xdrone] = Green OR Red Position(mycam); will return the X&Y locations of the drones position WRT color. 
[bwImgG,YGdrone,XGdrone] = GreenPosition(mycam);
[bwImgR,YRdrone,XRdrone] = RedPosition(mycam);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TURN ANGLE CALCULATION START
GreenPos = [XGdrone,YGdrone]; % OBSOLETE. MAY DELETE SOON

R_To_Gp_Dis = pdist([GreenPos(1),GreenPos(2);XRdrone,YRdrone] ,'euclidean'); %Red to new Green Position
R_To_Fp_Dis = pdist([XRdrone,YRdrone;flyToPoint(1),flyToPoint(2)] ,'euclidean'); %Red to flyToPoint
Gp_To_Fp_Dis = pdist([GreenPos(1),GreenPos(2);flyToPoint(1),flyToPoint(2)] ,'euclidean'); %new Green Position to flyToPoint


if flyToPoint(1) < GreenPos(1) %Determine if the fly to point is to the left of drone
    turnAngle = Determine_Angle(R_To_Gp_Dis, R_To_Fp_Dis, Gp_To_Fp_Dis);
     turnAngle = -turnAngle; %If so we need to turn left (counter clockwise/negative turnAngle)
else %Otherwise the fly to point is to the right of drone
    turnAngle = Determine_Angle(R_To_Gp_Dis, R_To_Fp_Dis, Gp_To_Fp_Dis); %We need to turn right (clockwise/positive turnAngle)
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TURN ANGLE CALCULATION END


flyDistance = Gp_To_Fp_Dis * (1/295); %Calculate actual flight distance in meters from pixel distance
%%% FROM MY OWN MEASUREMENTS: 1 meter is ~ 295 pixels. (Only for this particular set-up in the GCC research room)



% LIGHTS ON
r = ryze();%Connect to Drone and Make Drone Obj

speed = .5; %Meters/Sec
takeoff(r);

turn(r,deg2rad(turnAngle)); %Turn to face flyToPoint

moveforward(r, 'Distance', flyDistance, 'Speed', speed, 'WaitUntilDone', true);

land(r);







function [bwImg,XgreenCentre,YgreenCenter] = GreenPosition(mycam)

tim = tic;
duration = 2;
greenThreshold = 30;  %The "Green-ness" level
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


function [bwImg,XredCentre,YredCenter] = RedPosition(mycam)

tim = tic;
duration = 2;
redThreshold = 60;  %The "Red-ness" level
while(toc(tim) < duration)

img = snapshot(mycam);

    
%% Extract RGB color components from the FPV camera image
r = img(:,:,1);
g = img(:,:,2);
b = img(:,:,3);

%% Calculate the number of rows and coloumns in the FPV camera image
nRows = size(img, 1);
nCols = size(img, 2);

%% Approximate the intensity of red components in the image
redIntensities = r - g/2 - b/2;

%% Threshold the image to find the regions that we consider to be red enough
bwImg = redIntensities > redThreshold;

% Find indices of red pixels in the image
[row, col] = find(bwImg); %Where is the red? 

    
    % Find red pixels and track the ball using drone if there are enough red pixels in the image

    % Find center of the green ball in the captured image
    if ~isempty(row) && ~isempty(col)
        XredCentre = round(mean(row));
        YredCenter = round(mean(col));
        
%         if toc(tim) > 5  %Take a lookie at bwImg and playwith it with respect to red center (X,Y)
%             a = 2;
%         end
        

        imshow(bwImg)
    end



pause(0.1);
end

end




function [Deg_Angle] = Determine_Angle(a,b,c)

Deg_Angle = acosd( ( (a^2) + (b^2) - (c^2) )/( 2*a*b) );    %Modified law of cosines 

end


