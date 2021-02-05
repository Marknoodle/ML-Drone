

%%%% This file's purpose is to combine the functionalities of FlightPath.m
%%%% and Green_Track.m into one Fly and Camera Track Matlab script

%%%% CURRENT GOAL: Be able to fly drone and track position in real time
%%%% using green tracking algorithm AT THE SAME TIME. We also want to be
%%%% able to view the drawn path of the drone 
%%%% (so we need to find out how to 'preserve that figure' if we show both
%%%%  green tracking and path drawing at the same time)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%   STEP 1  (establish camera connection and preview)

mycam = webcam('j5 WebCam JVCU100');
preview(mycam)
   
figure;     %FIX FLIGHT PATH DRAWING FIGURE DISAPPERING ISSUE
hold on 

xlabel('x-axis (towards/away from white board)')            
ylabel('y-axis (going along the white board)')
zlabel('height of drone off ground');


%%%%%   STEP 2 (obtain flight path based off of the inputted verticies of a straight edge shape (inP) )

%Obtain Shape Points (sp)

trackPath = animatedline('LineWidth',2,"color","b"); %This is for drawing shape flight path before actual flight

%inP is the points of the shape given to us that we wish to fly
%inP = [[0 0]; [4 0]; [4 2]; [0 2]]; %This goes 4 meters forward, 2m left, 4m back, then 2m right (a 4 x 2 rectangle)

%For a Square Path use SquareLength (sL)
 sL = 1.2; %X meters on all sides
 inP = [[0 0]; [sL 0]; [sL sL]; [0 sL]]; 

sp = zeros(length(inP),2);

for i = 1:1:length(inP)
    sp(i,:) = inP(i,:);
    addpoints(trackPath, (sp(i)*400) + 200 , (sp(i,2)*400) + 200 ); %REPLACE WITH RED MARKER DISTANCE
end
addpoints(trackPath, sp(1)*400 + 200, sp(1,2)*400 + 200 ); 
% ^^^ Connects the last shape point to the first to "close the shape"

%%% HEADS-UP!!! All "*400 + 200" is for is to give a more accurate
%%% placement of shape with respect to where the droneLine will be drawn later


%Obtain Move Types Between Points and Move Distances
mvdis = zeros(length(sp),1);
for i = 1:1:length(sp)

    if i ~= length(sp) %movement between every point except last to first 
        if sp(i,1) ~= sp(i+1,1)
            if sp(i,1) - sp(i+1,1) < 0
                mvtype(i) = "mvf";
                mvdis(i) = sp(i+1,1) - sp(i,1);
            else 
                mvtype(i) = "mvb";
                mvdis(i) = sp(i,1) - sp(i+1,1);
            end 
        else 
            if sp(i,2) - sp(i+1,2) < 0
                mvtype(i) = "mvl";
                mvdis(i) = sp(i+1,2) - sp(i,2);
            else 
                mvtype(i) = "mvr";
                mvdis(i) = sp(i+1,2) - sp(i,2);
            end
        end 
    else %movement between last to first point
        if sp(i,1) ~= sp(1,1)
            if sp(i,1) - sp(1,1) < 0
                mvtype(i) = "mvf";
                mvdis(i) = sp(1,1) - sp(i,1);
            else 
                mvtype(i) = "mvb";
                mvdis(i) = sp(i,1) - sp(1,1);
            end 
        else 
            if sp(i,2) - sp(1,2) < 0
                mvtype(i) = "mvl";
                mvdis(i) = sp(1,2) - sp(i,2);
            else 
                mvtype(i) = "mvr";
                mvdis(i) = sp(i,2) - sp(1,2);
            end
        end
    end %if end
end %for end


r = ryze();%Connect to Drone and Make Drone Obj


%%%%%   STEP 3 (take off drone and move it vertically upward for better camera view) 

speed = 1; %Meters/Sec
takeoff(r);
moveup(r, 'Distance', 0.4) %the last arg just tells it to move a bit higher for better camera view

%%%%%   STEP 4 (fly flight path, run green tracking algorithm, and figure drawing at same time)

exeMvInstruction(length(sp),mvtype,mvdis,speed,r,mycam); 
land(r);
%clear
%%%END OF CODE%%%

function exeMvInstruction(instrNum,mvtype,mvdis,Speed,DroneObj,camObj)

    for i = 1:1:instrNum
        switch mvtype(i)
            case "mvf"
                moveforward(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
            case "mvb"
                moveback(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
            case "mvl"
                moveleft(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
            case "mvr"
                moveright(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
        end
        grnTrack(7,camObj,DroneObj); %Do green tracking for ___ seconds (right now set to 7)
        
    end
end 

function grnTrack(time,mycam,DroneObj) %%%Based off of Green_Track.m

droneLine = animatedline('LineWidth',2,"color","g");  
duration = time;
tim = tic;
greenThreshold = 40;  %The "Green-ness" level
minOffset = 30;
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
        height = readHeight(DroneObj);     %GIves us the 3rd height of drone dimension
        
        if( length(row) > 30 && length(col) > 30 && isvalid(droneLine) && ~isempty(height) && height ~= 0 ) 
            %length(row/col) is so we don't focus on small green things that the cam may pick up on.
            %isvalid(droneLine) is to avoid handle exception.
            %~isempty(height) && height ~= 0 is to ensure we get a more "correct" height reading of drone
        addpoints(droneLine, XgreenCentre, YgreenCenter, height ); %%%%%%%%%%%%%%%%% Add Green Location to be drawn
        end
        
        
        %Display original and binary image
        %subplot(1,2,1); imshow(img);
        %subplot(1,2,2); imshow(bwImg);

        %imshow(bwImg); % uncomment to see green tracking. WARNING!!! This will result in the drawing being lost. (to be fixed later)  
        drawnow; %drawn green location to figure
    end



pause(0.1);
end

end