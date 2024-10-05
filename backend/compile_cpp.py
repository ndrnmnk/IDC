import os
import subprocess


def compile_project(project_path, build_logs_widget):
    """
    Compiles a CMake project at the specified path while updating the build logs widget.

    :param project_path: The path to the CMake project to compile.
    :param build_logs_widget: QTextBrowser widget to display build logs.
    """

    # Prepare the build directory
    build_directory = os.path.join(project_path, 'build')
    os.makedirs(build_directory, exist_ok=True)

    # Change to the build directory
    os.chdir(build_directory)

    # Run CMake configuration
    try:
        build_logs_widget.append("Running CMake configuration...")
        subprocess.run(['cmake', project_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        build_logs_widget.append("CMake configuration successful.")
    except subprocess.CalledProcessError as e:
        build_logs_widget.append(f"CMake configuration failed: {e.stderr.decode()}")
        return

    # Run the build
    try:
        build_logs_widget.append("Starting build...")
        process = subprocess.Popen(['make'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Stream the output to the build_logs_widget
        for line in iter(process.stdout.readline, ''):
            build_logs_widget.append(line.strip())

        # Wait for the build to finish
        process.stdout.close()
        process.wait()

        if process.returncode == 0:
            build_logs_widget.append("Build completed successfully.")
        else:
            build_logs_widget.append(f"Build failed with return code: {process.returncode}")
            error_output = process.stderr.read()
            build_logs_widget.append(error_output.strip())
    except Exception as e:
        build_logs_widget.append(f"An error occurred: {str(e)}")
