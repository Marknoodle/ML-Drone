

%%%% This file's purpose was to get more familiar the matlab tello drone
%%%% support package, especially in reguards to flight navigation and
%%%% flight data collection

%%%%%%%% Code from: https://www.mathworks.com/help/supportpkg/ryzeio/ug/read-plot-navigation-data-using-matlab-support-package-for-ryze-tello-drones.html


takeoff(r);

%graph creation
 f = figure;
    hx = animatedline('Color', 'r', 'LineWidth', 2);
    hy = animatedline('Color', 'g', 'LineWidth', 2);
    hz = animatedline('Color', 'b', 'LineWidth', 2);
    title('DroneOrientation v/s Time');
    xlabel('Time (in s)');
    ylabel('Orientation (in degrees)');
    legend('XOrientation', 'YOrientation', 'ZOrientation');
    
   
   edgeIndex = 1; %Which edge of the 'square' we are on
   distance = 0.5; %Meters
   speed = 0.5; %Meters/Sec
   tObj = tic;
   while(edgeIndex <= 4)
       % Move the drone unblocking the command line
       tplot = tic;
       moveforward(r, 'Distance', distance, 'Speed', speed, 'WaitUntilDone', false);
       % Plot orientation while drone is moving
       while(toc(tplot)<distance/speed)
          orientation = rad2deg(readOrientation(r));
          tStamp = toc(tObj);
          addpoints(hx, tStamp, orientation(2));
          addpoints(hy, tStamp, orientation(3));
          addpoints(hz, tStamp, orientation(1));
          drawnow;
       end
      % Turn the drone after it has traversed one side of the square path
      pause(2);
      turn(r, deg2rad(90));
      
      edgeIndex = edgeIndex+1;
   end
   
   orientation = rad2deg(readOrientation(r));
    tStamp = toc(tObj);
    addpoints(hx, tStamp, orientation(2));
    addpoints(hy, tStamp, orientation(3));
    addpoints(hz, tStamp, orientation(1));
    drawnow;
    land(r);