

vid=VideoReader('Pat.mp4');% video we a ripping frames from (vid must be in directory)

%wrap in for loop later for each frame of vid  ( numFrames = vid.NumberOfFrames; )
frames = read(vid,1); %replace 1 with loop iterator
imwrite(frames,'fpic.jpg'); 
framePic = imread('fpic.jpg');
framePic_gray = rgb2gray(framePic);%pic has to be gray I think for SURF
framePic_pts = detectSURFFeatures(framePic_gray);




