

vid=VideoReader('bub_vid.mp4');% video we a ripping frames from (vid must be in directory)

%wrap in for loop later for each frame of vid  ( numFrames = vid.NumberOfFrames; )
frames = read(vid,1); %replace 1 with loop iterator
%imwrite(frames,'fpic.jpg'); 
%framePic = imread('fpic.jpg');
framePic_gray = rgb2gray(frames);%pic has to be gray for SURF
%framePic_pts = detectSURFFeatures(framePic_gray);


%imwrite(frames,'fpic.jpg');
%image = imread('fpic.jpg'); % MWsample_full.png %'bub_img.jpg'

