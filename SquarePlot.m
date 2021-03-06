
%%%% This file's purpose was to program the ryze tello drone to fly a
%%%% predetermined square flight path and to track the drone's postion with
%%%% the tello drone's internal speed sensors.


figure; 
xlabel('x-axis(out from camera) in meters')
ylabel('y-axis (perpendicular to camera in meters')
zlabel('z-axis (height) in meters') 

trackPath = animatedline('LineWidth',2,"color","b"); 
    
   distanceL = 2; %in meters, the length of one of the square sides we want the drone to fly

   %draw square with square points (sp) from squarepoints();
   sp = SquarePoints(distanceL); %square with length size 3
   spL = length(sp);
   for i = 1:1:spL
        addpoints(trackPath, sp(i), sp(i,2) );
   end
    
r = ryze(); %connect to drone (make sure you are on drone network)

pause(1); %in seconds

takeoff(r);

pause(1);

moveup(r,"Distance", 1.2, 'speed', 1);
   
   edgeIndex = 0; %Which edge of the 'shape' we are on
   speed = 1; %Meters/Sec

   drone = animatedline('LineWidth',2,"color","r"); %What gets plotted in real time on figure to represent drone movement
   
   leftoff = zeros(1:2); %Used to keep track of where drone was before new 'move' command
   
   while(edgeIndex <= 3) %each edge represents a path a drone will take from a specified move instruction
  
       switch edgeIndex
           case 0
               leftoff = moveWithPlotting(r, "forward", distanceL, speed, drone, leftoff, r); %forward
           case 1
               leftoff = moveWithPlotting(r, "forward", distanceL, speed, drone, leftoff, r); %right
           case 2
               leftoff = moveWithPlotting(r, "forward", distanceL, speed, drone, leftoff, r); %back
           case 3
               leftoff = moveWithPlotting(r, "forward", distanceL, speed, drone, leftoff, r); %left
       end %Flight path should resemble a square
      
      pause(2); %Make sure the drone has finished its current move command
      turn(r, pi/2); %turns drone 90 degrees to the right
      pause(1);%finish move command
      
      edgeIndex = edgeIndex+1; %moves to the next edge/move command
     
   end %add break point here when flying and wait for turn to finish before continuing for guaranteed good run
        
       % flip(r,'forward'); %Flip for joy!
      land(r);
      %clear; %end of this script, clears stored values
      %in the event that this script terminates prior to clear above, make
      %sure to manually clear before running this script again.

function position = moveWithPlotting(Drone, Direction, Distance, Speed, AnimatedLine, Position, droneObj) % Moving a specified direction, distance, and speed

    switch Direction
        case "forward"
            moveforward(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
        case "back"
            moveback(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
        case "right"
            moveright(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
        case "left"
            moveleft(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
    end
    position = plotPathing(Drone, AnimatedLine, Position, Distance, Speed, droneObj) %update where the drone 'should be' after move command (what gets put in leftoff)
end


function position = plotPathing(Drone, AnimatedLine, Position, Distance, Speed, droneObj) %plots the drone path on the figure 

    positionMemory = Position; %Last position of drone

    timeKeeper = tic; %timer start 
  
   
        while (toc(timeKeeper) < (Distance/Speed) + .1) % Until the drone finished its current move command
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



function sp = SquarePoints(SSL)

    rowIndex = 1;

    for i = 0:0.1:SSL
        sp(rowIndex,1) = i;
        rowIndex = rowIndex + 1; 
    end 

    for i = 0.1:0.1:SSL
        sp(rowIndex,1) = SSL;
        sp(rowIndex,2) = (i) ;
        rowIndex = rowIndex + 1; 
    end 

    for i = SSL:-0.1:0
        sp(rowIndex,1) = i;
        sp(rowIndex,2) = SSL;
        rowIndex = rowIndex + 1; 
    end 

    for i = SSL:-0.1:0
        sp(rowIndex,2) = i;
        rowIndex = rowIndex + 1; 
    end 

end
