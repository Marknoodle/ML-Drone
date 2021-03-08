
%%%% This file's purpose is to track green object movement in camera view
%%%% and plot/draw the movement to a graph

%%%%%%%% Code from: https://www.mathworks.com/help/supportpkg/ryzeio/ug/track-a-green-ball-using-ryze-drone.html

%%%%%%% Modified trackBall.m code

%ryzeObj = ryze();
%cameraObj = camera(ryzeObj);
mycam = webcam('j5 WebCam JVCU100'); %%% The argument is the usb camera in the research room: 'j5 WebCam JVCU100'
preview(mycam)



droneLine = animatedline('LineWidth',2,"color","r");         
figure;     %DO NOT CLICK FIGURE DURING TRACKING. DO NOT!!!

%%% FIX THE FIGURE PROBLEM


%Assuming Camera is level
xlabel('x-axis(out from camera) in meters')
ylabel('y-axis (perpendicular to camera in meters')


tim = tic;
duration = 7;
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
        
%         if toc(tim) > 5  %Take a lookie at bwImg and playwith it with respect to green center (X,Y)
%             a = 2;
%         end
        
        if length(row) > 299 && length(col) > 299      
        addpoints(droneLine, XgreenCentre, YgreenCenter ); %%%%%%%%%%%%%%%%% Plot Green Location
        end
        
        % Find the displacement of the green ball from the centre of the
        % image
        rowOffset = (nRows/2) - XgreenCentre;
        colOffset = (nCols/2) - YgreenCenter;
        
        % Display original and binary image
        %subplot(1,2,1); imshow(img);
        %subplot(1,2,2); imshow(bwImg);
        plot(1); 
        imshow(bwImg)
        drawnow;
    end



pause(0.1);
end



