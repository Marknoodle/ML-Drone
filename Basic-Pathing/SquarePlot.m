r = ryze();

pause(3);

takeoff(r);

figure;
xlabel('x-axis')
ylabel('y-axis')
%zlabel('z-axis')
   
   edgeIndex = 0; %Which edge of the 'square' we are on
   distanceL = 0.5; %Meters

   speed = 0.5; %Meters/Sec
   
   drone = animatedline('LineWidth',2,"color","r");
   
   leftoff = zeros(1:2);
   
  % totalDistance = distanceL * 4 in this case
   while(edgeIndex <= 3)
       tplot = tic;
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
      %turn(r, pi/2);
      
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
    stopWatch = tic;
    position = plotPathing(Drone, AnimatedLine, axis, stopWatch, Position)
end


function position = plotPathing(Drone, AnimatedLine, Axis, TimeKeeper, Position)
    pause(0.1)
    positionMemory = Position;
    [speed, ~] = readSpeed(Drone);
    speedInX = speed(1);
    speedInY = speed(2);
    switch Axis
        case "x"
            while (speedInX > 0)
                [speed, ~] = readSpeed(Drone);
                speedInX = speed(1);
                speedInY = speed(2);
                timeStamp = toc(TimeKeeper);
                addpoints(AnimatedLine, positionMemory(1) + timeStamp * speedInX, positionMemory(2) + timeStamp * speedInY);
                drawnow;
            end
        case "y"
            while (speedInY > 0)
                [speed, ~] = readSpeed(Drone);
                speedInX = speed(1);
                speedInY = speed(2);
                timeStamp = toc(TimeKeeper);
                addpoints(AnimatedLine, positionMemory(1) + timeStamp * speedInX, positionMemory(2) + timeStamp * speedInY);
                drawnow;
            end
    end
    position = [timeStamp * speedInX, timeStamp * speedInY];
end