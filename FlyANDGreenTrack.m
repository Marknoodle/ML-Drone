

%%%% This file's purpose is to combine the functionalities of FlightPath.m
%%%% and Green_Track.m into one Fly and Camera Track Matlab script

%%%% CURRENT GOAL: Be able to fly drone and track position in real time
%%%% using green tracking algorithm AT THE SAME TIME. We also want to be
%%%% able to view the drawn path of the drone (so we need to find out how
%%%% to 'preserve that figure'

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%   STEP 1  (establish camera connection and preview)

mycam = webcam('j5 WebCam JVCU100');
preview(mycam)

%%%%%%%%%%%%%%%%% FIX FLIGHT PATH DRAWING FIGURE DISAPPERING ISSUE

%droneLine = animatedline('LineWidth',2,"color","r");    
figure;     %DO NOT CLICK FIGURE DURING TRACKING. DO NOT!!!
hold on 

xlabel('x-axis(out from camera) in meters')             %Needs to be changed
ylabel('y-axis (perpendicular to camera in meters')     %Needs to be changed

%%%%%%%%%%%%%%%%% FIX FLIGHT PATH DRAWING FIGURE DISAPPERING ISSUE


%%%%%   STEP 2 (obtain flight path based off of the inputted verticies of a straight edge shape (inP) )

%Obtain Shape Points (sp)

%inP is the points of the shape given to us that we wish to fly
%inP = [[0 0]; [4 0]; [4 2]; [0 2]]; %This goes 4 meters forward, 2m left, 4m back, then 2m right (a 4 x 2 rectangle)

%For a Square Path use SquareLength (sL)
 sL = 1.2; %2 meters on all sides
 inP = [[0 0]; [sL 0]; [sL sL]; [0 sL]]; 

sp = zeros(length(inP),2);

for i = 1:1:length(inP)
    sp(i,:) = inP(i,:);
end

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
moveup(r, 'Distance', 0.6)

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
        grnTrack(7,camObj); %Do green tracking for ___ seconds
        
    end
end 

function grnTrack(time,mycam) %%%Based off of Green_Track.m

droneLine = animatedline('LineWidth',2,"color","r");  
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
        
        if length(row) > 299 && length(col) > 299 && isvalid(droneLine)
        addpoints(droneLine, XgreenCentre, YgreenCenter ); %%%%%%%%%%%%%%%%% Plot Green Location
        end
        
        % Find the displacement of the green ball from the centre of the
        % image
        rowOffset = (nRows/2) - XgreenCentre;
        colOffset = (nCols/2) - YgreenCenter;
        
        % Display original and binary image
        %subplot(1,2,1); imshow(img);
        %subplot(1,2,2); imshow(bwImg);
        plot(1); imshow(bwImg);
        drawnow;
    end



pause(0.1);
end

end