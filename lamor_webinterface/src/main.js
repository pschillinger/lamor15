window.onload = function() {
	RC.ROS.trySetupConnection();
	
	document.getElementById('yes_button').addEventListener('click', RC.PubSub.sendDialogYes);
	document.getElementById('no_button').addEventListener('click', RC.PubSub.sendDialogNo);
}