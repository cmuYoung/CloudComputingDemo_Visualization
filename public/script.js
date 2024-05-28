// Function to start recording
function startRecording() {
    document.getElementById("navi").style.display = 'block';
    var url = document.getElementById("urlstart").value;

    GazeCloudAPI.StartEyeTracking();
    GazeCloudAPI.OnCalibrationComplete = function () {
        GazeRecorderAPI.Rec(url);
    };
}

// Function to navigate
function navigate() {
    var url = document.getElementById("url").value;
    GazeRecorderAPI.Navigate(url);
}

// Function to play recorded data
function playRecording() {
    document.getElementById("navi").style.display = 'none';
    GazeRecorderAPI.StopRec();
    GazeCloudAPI.StopEyeTracking();

    GazePlayer.SetCountainer(document.getElementById("playerdiv"));
    var sessionReplayData = GazeRecorderAPI.GetRecData();
    GazePlayer.PlayResultsData(sessionReplayData);
}

