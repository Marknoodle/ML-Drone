takeoff(r);

figure;
xlabel('x-axis')
ylabel('y-axis')
zlabel('z-axis')
   
   edgeIndex = 1; %Which edge of the 'square' we are on
   distance = 0.5; %Meters
   speed = 0.5; %Meters/Sec
   tObj = tic;
   
   drone = animatedline('LineWidth',2);
   
   while(edgeIndex <= 2)
       % Move the drone unblocking the command line
       tplot = tic;
       moveforward(r, 'Distance', distance, 'Speed', speed, 'WaitUntilDone', false);
       timey = tic; %timer to keep track of how long since 'moveforward()'
       % Plot orientation while drone is moving
       while(toc(tplot)<distance/speed) %determins if we have gone full mf distance
          [speedz,timen] = readSpeed(r);
          tStamp = toc(timey);
          addpoints(drone, (tStamp*speedz(1)),(tStamp*speedz(2)), readHeight(r) );
          drawnow;
          %plot3( (tStamp*speedz(1)),(tStamp*speedz(2)), readHeight(r));
            %Watch out for array elements issue (current fix is to just
            %redo)
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