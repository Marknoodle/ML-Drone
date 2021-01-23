
%%%% This file's purpose is to give the tello drone a predetermined flight
%%%% path based off of the inputted verticies of a straight edge shape (inP)

%Obtain Shape Points (sp)

%inP is the points of the shape given to us that we wish to fly
inP = [[0 0]; [4 0]; [4 2]; [0 2]]; %This goes 4 meters forward, 2m left, 4m back, then 2m right (a 4 x 2 rectangle)

%For a Square Path use SquareLength (sL)
% sL = 2; %2 meters on all sides
% inP = [[0 0]; [sL 0]; [sL sL]; [0 sL]]; 

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
speed = 1; %Meters/Sec
takeoff(r);

exeMvInstruction(length(sp),mvtype,mvdis,speed,r);
land(r);
clear
%%%END OF CODE%%%

function exeMvInstruction(instrNum,mvtype,mvdis,Speed,DroneObj)

    for i = 1:1:instrNum
        switch mvtype(i)
            case "mvf"
                moveforward(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', true);
            case "mvb"
                moveback(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', true);
            case "mvl"
                moveleft(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', true);
            case "mvr"
                moveright(DroneObj, 'Distance', mvdis(i,1), 'Speed', Speed, 'WaitUntilDone', true);
        end

    end
end 





