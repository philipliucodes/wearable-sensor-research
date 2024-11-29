% Define the path to the spectrogram dataset
digitDatasetPath = "/MATLAB Drive/Matlab_Audio_Spectrograms";

% Load the dataset with imageDatastore
digitData = imageDatastore(digitDatasetPath, ...
    'IncludeSubfolders', true, ...
    'LabelSource', 'foldernames');

% Display data properties for verification
disp("Loaded file paths:");
disp(digitData.Files);
disp("Loaded class labels:");
disp(digitData.Labels);

% Split the dataset into training, validation, and testing sets
[trainDigitData, validDigitData, testDigitData] = splitEachLabel(digitData, 0.7, 0.1, "randomized");

% Load the pretrained AlexNet
net = alexnet;

% Prepare data augmentation and resizing
inputSize = net.Layers(1).InputSize;
imageAugmenter = imageDataAugmenter('RandXReflection', true);

auimdstrain = augmentedImageDatastore(inputSize, trainDigitData, ...
    'ColorPreprocessing', 'gray2rgb', ...
    'DataAugmentation', imageAugmenter);

auimdstest = augmentedImageDatastore(inputSize, testDigitData, ...
    'ColorPreprocessing', 'gray2rgb');

auimdsvalid = augmentedImageDatastore(inputSize, validDigitData, ...
    'ColorPreprocessing', 'gray2rgb');

% Modify AlexNet for transfer learning
layersTransfer = net.Layers(1:end-3);
numClasses = numel(categories(trainDigitData.Labels));

layers = [
    layersTransfer
    dropoutLayer(0.5)  % Add a dropout layer
    fullyConnectedLayer(numClasses, 'WeightLearnRateFactor', 20, 'BiasLearnRateFactor', 20)
    softmaxLayer
    classificationLayer];

% Training options
optionsTransfer = trainingOptions('sgdm', ...
    'Momentum', 0.9, ...
    'InitialLearnRate', 0.0005, ...
    'LearnRateDropFactor', 0.1, ...
    'LearnRateDropPeriod', 10, ...
    'L2Regularization', 0.0001, ...
    'GradientThresholdMethod', 'l2norm', ...
    'GradientThreshold', Inf, ...
    'MaxEpochs', 60, ...
    'MiniBatchSize', 32, ...
    'Verbose', 1, ...
    'VerboseFrequency', 50, ...
    'Plots', 'training-progress', ...
    'ValidationData', auimdsvalid, ...
    'ValidationFrequency', 10);

% Train the model
disp("Training the model...");
netTransfer = trainNetwork(auimdstrain, layers, optionsTransfer);

% Test the model
disp("Testing the model...");
[YPred, p] = classify(netTransfer, auimdstest);
YTest = testDigitData.Labels;

% Calculate accuracy
accuracy = sum(YPred == YTest) / numel(YTest);
disp("Test Accuracy:");
disp(accuracy);

% Save predictions and the trained model
writematrix([YPred, YTest], 'SensorPredictions_ActualValues.csv');
save('trainedModelSensor.mat', 'netTransfer');

% Save confusion matrix as an image
confMat = confusionchart(YTest, YPred);
saveas(confMat, 'ConfusionMatrixSensor.png');
