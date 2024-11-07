import subprocess






def run_command(command, logs_widget):
	# Create a CommandRunner instance
	runner = CommandRunner(command, logs_widget)

	# Connect the signal to the function that updates the logs_widget
	runner.output_signal.connect(lambda text: logs_widget.append(text))

	# Start the thread to run the command in the background
	runner.start()
