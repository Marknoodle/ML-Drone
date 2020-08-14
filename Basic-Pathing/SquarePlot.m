r = ryze(); %connect to drone (make sure you are on drone network)

pause(2); %in seconds

takeoff(r);

figure; 
xlabel('x-axis')
ylabel('y-axis')
%zlabel('z-axis') %Trying to focus on just 2 Dimensions for now 
% (not yet considering drone height when graphing)
   
   edgeIndex = 0; %Which edge of the 'shape' we are on
   distanceL = 0.5; %Meters

   speed = 0.5; %Meters/Sec
   
   drone = animatedline('LineWidth',2,"color","r"); %What gets plotted in real time on figure to represent drone movement
   
   leftoff = zeros(1:2); %Used to keep track of where drone was before new 'move' command
   
   while(edgeIndex <= 3) %each edge represents a path a drone will take from a specified move instruction
  
       switch edgeIndex
           case 0
               leftoff = moveWithPlotting(r, "forward", distanceL, speed, drone, leftoff); %forward
           case 1
               leftoff = moveWithPlotting(r, "right", distanceL, speed, drone, leftoff); %right
           case 2
               leftoff = moveWithPlotting(r, "back", distanceL, speed, drone, leftoff); %back
           case 3
               leftoff = moveWithPlotting(r, "left", distanceL, speed, drone, leftoff); %left
       end %Flight path should resemble a square
      
      pause(2); %Make sure the drone has finished its current move command
      
      edgeIndex = edgeIndex+1; %moves to the next edge/move command
   end
   
      land(r);
      clear; %end of this script, clears stored values
      %in the event that this script terminates prior to clear above, make
      %sure to manually clear before running this script again.

function position = moveWithPlotting(Drone, Direction, Distance, Speed, AnimatedLine, Position) % Moving a specified direction, distance, and speed

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
    position = plotPathing(Drone, AnimatedLine, Position, Distance, Speed) %update where the drone 'should be' after move command (what gets put in leftoff)
end


function position = plotPathing(Drone, AnimatedLine, Position, Distance, Speed) %plots the drone path on the figure 

    positionMemory = Position; %Last position of drone

    timeKeeper = tic; %timer start 
  
   
        while (toc(timeKeeper) < Distance/Speed) % Until the drone finished its current move command
                [speed, ~] = readSpeed(Drone);%retrieve current moving speed of drone
                speedInX = speed(1); %speed in x direction
                speedInY = speed(2); %speed in y direction 
                elapsedTime = toc(timeKeeper); %how much time has passed since drone has begun to move after command 
                addpoints(AnimatedLine, positionMemory(1) + elapsedTime * speedInX, positionMemory(2) + elapsedTime * speedInY); %trying to record updated drone distances in real time
                drawnow; %The idea is that if you multiply elapsedTime by x and y speed you can find out the distance the drone has traveled
        end
            
    position = [elapsedTime * speedInX, elapsedTime * speedInY]; % returns our updated position in the x and y axis
    %if we did not have 'position' all future updates to the figure would start
    %at origin and not where the drone left off 
    %'position' is what eventually gets stored in leftoff
end