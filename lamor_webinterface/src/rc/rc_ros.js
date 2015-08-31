RC.ROS = new (function() {
	var that = this;

	var ros;
	var connected = false;
	var connect_attempts_left = 0;

	this.getROS = function() {
		return ros;
	}

	var setupConnection = function() {
		connected = true;
		ros.on('error', setupFailed);
		ros.on('close', connectionClosed);

		RC.PubSub.initialize(ros);
	}

	var setupFailed = function() {
		
	}

	var connectionClosed = function() {
		RC.PubSub.shutdown();
		connected = false;
	}

	var attemptToConnect = function() {
		ros = new ROSLIB.Ros({
			url : 'ws://linda:8088'
		});
		ros.on('connection', setupConnection);
		ros.on('error', function() {
			connect_attempts_left--;
			console.log(connect_attempts_left);
			if (connect_attempts_left > 0) {
				setTimeout(attemptToConnect, 1000);
			} else {
				setupFailed();
			}
		});
	}

	this.trySetupConnection = function() {
		connect_attempts_left = 10;
		attemptToConnect();
	}

	this.closeConnection = function() {
		ros.close();
	}

	this.isConnected = function() {
		return connected;
	}

}) ();