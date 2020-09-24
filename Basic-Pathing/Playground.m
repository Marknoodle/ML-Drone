
%%%%Obtain Shape Points (sp)

%inP is the points of the shape given to us that we wish to fly
%inP = [[0 0]; [4 0]; [4 2]; [0 2]]; %This goes 4 meters forward, 2m left, 4m back, then 2m right (a 4 x 2 rectangle)

%For a Square Path use SquareLength (sL)
 sL = 1; %2 meters on all sides
 inP = [[0 0]; [sL 0]; [sL sL]; [0 sL]]; 

sp = zeros(length(inP),2); %Pre-allocation of space for Shape points

for i = 1:1:length(inP) %Take every point in inP and putting them in sp 
    sp(i,:) = inP(i,:);
end

%%%%Obtain Move Types Between Points, Move Distances And Obtain (.1m) Line Points/Graphing List
mvdis = zeros(length(sp),1);%Pre-allocation of space for Shape points
rowindex = 1;%Row index variable for lines 
mvtype = "Pre-Allocation"; %Pre-allocation of space for move types
lines = zeros(1,2); %Pre-allocation of space for lines


for i = 1:1:length(sp) %For every point in the shape

    if i ~= length(sp) %movement between every point except last to first 
        if sp(i,1) ~= sp(i+1,1)%change from this point to next is change in x direction
            if sp(i,1) - sp(i+1,1) < 0 
                mvtype(i) = "mvf"; 
                mvdis(i) = sp(i+1,1) - sp(i,1);
                    for j = sp(i,1):0.1:sp(i+1,1) %X-values
                    lines(rowindex,1) = j;
                    lines(rowindex,2) = sp(i,2);
                    rowindex = rowindex + 1;
                    end             
            else 
                mvtype(i) = "mvb";
                mvdis(i) = sp(i,1) - sp(i+1,1);
                    for j = sp(i+1,1):0.1:sp(i,1) %X-values
                    lines(rowindex,1) = sp(i,1)-j;
                    lines(rowindex,2) = sp(i,2);
                    rowindex = rowindex + 1;
                    end
            end 
        else %change from this point to next is change in y direction
            if sp(i,2) - sp(i+1,2) < 0
                mvtype(i) = "mvl";
                mvdis(i) = sp(i+1,2) - sp(i,2);
                    for j = sp(i,2):0.1:sp(i+1,2) %Y-values
                    lines(rowindex,2) = j; 
                    lines(rowindex,1) = sp(i,1);
                    rowindex = rowindex + 1;
                    end
            else 
                mvtype(i) = "mvr";
                mvdis(i) = sp(i+1,2) - sp(i,2);
                    for j = sp(i+1,2):0.1:sp(i,2) %Y-values
                    lines(rowindex,2) = sp(i,2)-j;
                    lines(rowindex,1) = sp(i,1);
                    rowindex = rowindex + 1;
                    end
            end
        end 
    else %movement between last to first point
        if sp(i,1) ~= sp(1,1)
            if sp(i,1) - sp(1,1) < 0
                mvtype(i) = "mvf";
                mvdis(i) = sp(1,1) - sp(i,1);
                    for j = sp(i,1):0.1:sp(1,1) %X-values
                    lines(rowindex,1) = j;
                    lines(rowindex,2) = sp(i,2);
                    rowindex = rowindex + 1;
                    end
            else 
                mvtype(i) = "mvb";
                mvdis(i) = sp(i,1) - sp(1,1);
                    for j = sp(1,1):0.1:sp(i,1) %X-values
                    lines(rowindex,1) = sp(i,1)-j;
                    lines(rowindex,2) = sp(i,2);
                    rowindex = rowindex + 1;
                    end
            end 
        else 
            if sp(i,2) - sp(1,2) < 0
                mvtype(i) = "mvl";
                mvdis(i) = sp(1,2) - sp(i,2);   
                    for j = sp(i,2):0.1:sp(1,2) %Y-values
                    lines(rowindex,2) = j; 
                    lines(rowindex,1) = sp(i,1);
                    rowindex = rowindex + 1;
                    end
            else 
                mvtype(i) = "mvr";
                mvdis(i) = sp(i,2) - sp(1,2);
                    for j = sp(1,2):0.1:sp(i,2) %Y-values
                    lines(rowindex,2) = sp(i,2)-j;
                    lines(rowindex,1) = sp(i,1);
                    rowindex = rowindex + 1;
                    end
            end
        end
    end %if end
end %for end


%%%%Graphing The Path Shape
figure; 
xlabel('x-axis(out from camera) in meters')
ylabel('y-axis (perpendicular to camera in meters')
zlabel('z-axis (height) in meters') 

%%%%Plotting all the path line points
linePoints = animatedline('LineWidth',2,"color","b");
for i = 1:1:length(lines)
    addpoints(linePoints,lines(i,1),lines(i,2)); 
end

droneLine = animatedline('LineWidth',2,"color","r"); %animated line for drone 

%%%%Begin take off instruction
r = ryze();%Connect to Drone and Make Drone Obj
speed = 1; %Meters/Sec
leftOff = zeros(1:2); %Used to keep track of where drone was before new 'move' command
takeoff(r);

%Execute Path Flight
exeMvInstruction(length(sp),mvtype,mvdis,speed,r,leftOff,droneLine);
land(r);
clear
%%%END OF CODE%%%

function exeMvInstruction(instrNum,mvtype,mvdis,Speed,droneObj,leftOff,droneLine)

    for i = 1:1:instrNum
        switch mvtype(i)
            case "mvf"
                moveforward(droneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
            case "mvb"
                moveback(droneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
            case "mvl"
                moveleft(droneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
            case "mvr"
                moveright(droneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', false);
        end
        leftOff = plotPathing(droneLine, leftOff, mvdis(i,1), Speed, droneObj); %update where the drone 'should be' after move command (what gets put in leftoff)
        pause(3)
    end
end 


function position = plotPathing(AnimatedLine, Position, Distance, Speed, droneObj) %plots the drone path on the figure 

    positionMemory = Position; %Last position of drone

    timeKeeper = tic; %timer start 
  
   
        while (toc(timeKeeper) < Distance/Speed) % Until the drone finished its current move command
                speed = readSpeed(droneObj);
                height = readHeight(droneObj);
                if(~isempty(speed) && ~isempty(height) && height ~= 0) %Sometimes speed will be a flat zero, which will crash when adding points.
                    %speed(1); speed in x direction
                    %speed(2); speed in y direction 
                    elapsedTime = toc(timeKeeper); %how much time has passed since drone has begun to move after command 
                    addpoints(AnimatedLine, positionMemory(1) + elapsedTime * speed(1), positionMemory(2) + elapsedTime * speed(2), height ); %trying to record updated drone distances in real time
                    drawnow; %The idea is that if you multiply elapsedTime by x and y speed you can find out the distance the drone has traveled
                end 
        end
            
    position = [positionMemory(1) + elapsedTime * speed(1), positionMemory(2) + elapsedTime * speed(2)]; % returns our updated position in the x and y axis
    %if we did not have 'position' all future updates to the figure would start
    %at origin and not where the drone left off 
    %'position' is what eventually gets stored in leftoff
end


