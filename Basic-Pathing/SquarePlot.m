r = ryze(); %connect to drone (make sure you are on drone network)

pause(3); 

takeoff(r);

figure;
xlabel('x-axis')
ylabel('y-axis')
%zlabel('z-axis')
   
   edgeIndex = 0; %Which edge of the 'shape' we are on
   distanceL = 0.5; %Meters

   speed = 0.5; %Meters/Sec
   
   drone = animatedline('LineWidth',2,"color","r"); %What gets plotted in real time on figure to represent drone movement
   
   leftoff = zeros(1:2); %Used to keep track of where drone was before new 'move' command
   
  % totalDistance = distanceL * 4 in this case
   while(edgeIndex <= 3)
       %tplot = tic;
       switch edgeIndex
           case 0
               leftoff = moveWithPlotting(r, "forward", distanceL, speed, drone, leftoff);
           case 1
               leftoff = moveWithPlotting(r, "right", distanceL, speed, drone, leftoff);
           case 2
               leftoff = moveWithPlotting(r, "back", distanceL, speed, drone, leftoff);
           case 3
               leftoff = moveWithPlotting(r, "left", distanceL, speed, drone, leftoff);
       end
      
      pause(2);
      
      edgeIndex = edgeIndex+1;
   end
   
      land(r);
      clear;

function position = moveWithPlotting(Drone, Direction, Distance, Speed, AnimatedLine, Position)

    switch Direction
        case "forward"
            moveforward(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
            axis = "x";
        case "back"
            moveback(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
            axis = "x";
        case "right"
            moveright(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
            axis = "y";
        case "left"
            moveleft(Drone, 'Distance', Distance, 'Speed', Speed, 'WaitUntilDone', false);
            axis = "y";
    end
    position = plotPathing(Drone, AnimatedLine, axis, Position, Distance, Speed)
end


function position = plotPathing(Drone, AnimatedLine, Axis,  Position, Distance, Speed)
    pause(0.1);
    positionMemory = Position;
    [speed, ~] = readSpeed(Drone);
    speedInX = speed(1);
    speedInY = speed(2);
    TimeKeeper = tic;
    elapsedTime = 0;
    %while(speedInX == speedInY && speedInX == 0) %Do not want to record information until drone is moving
          %waiting 
    %end
    %switch Axis
        
        % case that runs dependent on speed in the X-Axis
        %case "x" 
        while (toc(timeKeeper) < Distance/Speed)
                [speed, ~] = readSpeed(Drone);
                speedInX = speed(1);
                speedInY = speed(2);
                elapsedTime = toc(TimeKeeper);
                addpoints(AnimatedLine, positionMemory(1) + elapsedTime * speedInX, positionMemory(2) + elapsedTime * speedInY);
                drawnow;
        end
            
        % case that runs dependent on speed in the Y-Axis
      %  case "y"
      %      while (speedInY > 0)                                                     % while we are still moving
      %          [speed, ~] = readSpeed(Drone);                                       % stores the current speed of the drone in the speed variable, tosses out the current time
      %          speedInX = speed(1);                                                 % speed in x-axis -> speedInX
      %          speedInY = speed(2);                                                 % speed in y-axis -> speedInY
      %          elapsedTime = toc(TimeKeeper);                                       % calculates the elapsed time since the last tick -> elapsedTime
      %          addpoints(AnimatedLine, positionMemory(1) + elapsedTime * speedInX, positionMemory(2) + elapsedTime * speedInY); % adds an x and y point to our animated line
      %          drawnow; % draws the updated animated line
     %       end
    %end
    position = [elapsedTime * speedInX, elapsedTime * speedInY]; % returns our updated position in the x and y axis
end