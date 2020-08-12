r = ryze();

pause(3);

takeoff(r);

figure;
xlabel('x-axis')
ylabel('y-axis')
%zlabel('z-axis')
   
   edgeIndex = 0; %Which edge of the 'square' we are on
   distanceL = 0.5; %Meters
   distanceS = 0.25;
   speed = 0.5; %Meters/Sec
   tObj = tic;
   
   drone = animatedline('LineWidth',2,"color","r");
   
   leftoff = zeros(1:2);
   
  % totalDistance = distance
   speedz = 0;
   while(edgeIndex <= 3)
       % Move the drone unblocking the command line
       tplot = tic;
       if (edgeIndex == 0)
            moveforward(r, 'Distance', distanceL, 'Speed', speed, 'WaitUntilDone', false);
            timey = tic; %timer to keep track of how long since 'moveforward()'
            [speedz,timen] = readSpeed(r);
            % Plot orientation while drone is moving
            while() %determins if we have gone full mf distance
                [speedz,timen] = readSpeed(r);
                tStamp = toc(timey);
                addpoints(drone, (leftoff(1) + tStamp*speedz(1)),(leftoff(2) + tStamp*speedz(2)) );
                drawnow;
            end
            leftoff(1) = leftoff(1) + distanceL;
       elseif (edgeIndex == 1)
            moveright(r, 'Distance', distanceS, 'Speed', speed, 'WaitUntilDone', false);
            timey = tic; %timer to keep track of how long since 'moveforward()'
            % Plot orientation while drone is moving
            while(readSpeed(r) > 0) %determins if we have gone full mf distance
                [speedz,timen] = readSpeed(r);
                tStamp = toc(timey);
                addpoints(drone, (leftoff(1) + tStamp*speedz(1)), (leftoff(2) + tStamp*speedz(2)) );
                drawnow;
            end
            leftoff(2) = leftoff(2) + distanceS;
       elseif (edgeIndex == 2)
            moveback(r, 'Distance', distanceL, 'Speed', speed, 'WaitUntilDone', false);
            timey = tic; %timer to keep track of how long since 'moveforward()'
            % Plot orientation while drone is moving
            while(readSpeed(r) > 0) %determins if we have gone full mf distance
                [speedz,timen] = readSpeed(r);
                tStamp = toc(timey);
                addpoints(drone, (leftoff(1) + tStamp*speedz(1)),(leftoff(2) + tStamp*speedz(2)) );
                drawnow;
            end
            leftoff(1) = leftoff(1) - distanceL;
       elseif (edgeIndex == 3)
            moveleft(r, 'Distance', distanceS, 'Speed', speed, 'WaitUntilDone', false);
            timey = tic; %timer to keep track of how long since 'moveforward()'
            % Plot orientation while drone is moving
            while(readSpeed(r) > 0) %determins if we have gone full mf distance
                [speedz,timen] = readSpeed(r);
                tStamp = toc(timey);
                addpoints(drone, (leftoff(1) + tStamp*speedz(1)),(leftoff(2) + tStamp*speedz(2)) );
                drawnow;
            end
            leftoff(2) = leftoff(2) - distanceS;
       end
        
      % Turn the drone after it has traversed one side of the square path
      clear timey;
      clear speedz;
      clear timen;
      clear tstamp;
      
      
      pause(5);
      %turn(r, pi/2);
      
      edgeIndex = edgeIndex+1;
   end
   
      land(r);
      clear;