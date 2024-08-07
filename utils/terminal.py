import re
import subprocess
from GLOBAL import GLOBAL


class Terminal:

    @staticmethod
    def execute_command(command):
        """Open PowerShell and execute a command."""
        try:

            # Execute command in PowerShell
            # We use '/c' to run the command and terminate
            result = subprocess.run(['powershell', '-Command', command], shell=True)
            return result

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def available_system_images():
        """List available system images using sdkmanager."""
        try:
            result = subprocess.run([GLOBAL.PATH.SDK_MANAGER_PATH, '--list'], capture_output=True, text=True,
                                    check=True)
            # Filter lines that contain 'system-images\'
            system_images = [line for line in result.stdout.splitlines() if 'system-images\\' in line]
            formatted_system_images = []
            for system_image_string in system_images:
                parts = [part.strip() for part in system_image_string.split('|')]
                if len(parts) == 4:
                    program_name = parts[0]
                    num = parts[1]
                    human_name = parts[2]
                    path = parts[3]
                    formatted_system_images.append({'program_name': program_name, 'num': num, 'human_name': human_name,path: path})

            return formatted_system_images
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Output: {e.output}")
            print(f"Error: {e.stderr}")

    @staticmethod
    def list_available_devices():
        """List available devices using avdmanager."""
        try:
            result = subprocess.run([GLOBAL.PATH.AVD_MANAGER_PATH, 'list', 'devices'], capture_output=True, text=True,
                                    check=True)
            list_devices = [re.search(r'"([^"]*)"', line).group(1) for line in result.stdout.splitlines() if 'id: ' in line]
            return list_devices
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Output: {e.output}")
            print(f"Error: {e.stderr}")

    @classmethod
    def install_default_system_image(cls):
        """Install the System Image: sdkmanager "system-images;android-35;google_apis_playstore_ps16k;x86_64"."""
        result = cls.execute_command(
            f'{GLOBAL.PATH.SDK_MANAGER_PATH} --install "system-images;android-35;google_apis_playstore_ps16k;x86_64"')
        return result



"""
test
"""
if __name__ == '__main__':
    terminal = Terminal()
    print(terminal.execute_command(
        f'{GLOBAL.PATH.CMDLINE_TOOLS_PATH}\\avdmanager.bat create avd -n test3 -k "system-images;android-35;google_apis_playstore_ps16k;x86_64" -d pixel_6'))

    print(terminal.available_system_images())
    print(terminal.list_available_devices())
