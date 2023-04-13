# Adding a Command to Run at Boot on a Linux Machine

## Using /etc/rc.local

1. Open a terminal on the Linux machine.
2. Edit the `/etc/rc.local` file using a text editor such as `nano` or `vi`. This file contains commands that are executed at the end of the boot process.

```bash
    sudo nano /etc/rc.local
```

3. Add the command that you want to execute at boot to the file, before the `exit 0` line. For example:

```bash
    /usr/bin/python /home/pi/gitHub/RPi-TMon-MQTT/RPi-TMon-MQTT.py&
```

Note the `&` at the end of the command which puts it in the background and allows the boot process to continue.

4. Save the file and exit the text editor.
5. Make the `/etc/rc.local` file executable:

```bash
    sudo chmod +x /etc/rc.local
```

6. Reboot the Linux machine to test if the command is executed at boot.

## Using systemd
### Create the systemd service

1. Create a systemd service file using a text editor such as `nano` or `vi`. For example:

```bash
    sudo nano /etc/systemd/system/rpi-tmon-mqtt.service
```

2. Add the following content to the file:

```bash
    [Unit]
    Description=RPi-TMon-MQTT service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python /home/pi/gitHub/RPi-TMon-MQTT/RPi-TMon-MQTT.py
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target
```

This creates a service that will start the command at boot and restart it if it fails.

3. Save the file and exit the text editor.
4. Reload the systemd daemon to read the new service file:

```bash
    sudo systemctl daemon-reload
```

5. Enable the service to start at boot:

```bash
    sudo systemctl enable rpi-tmon-mqtt.service
```

6. Start the service:

```bash
    sudo systemctl start rpi-tmon-mqtt.service
```

7. Reboot the Linux machine to test if the command is executed at boot.



### Removing the systemd Service

1. Open a terminal on the Linux machine.
2. Disable the service from starting at boot:

```bash
    sudo systemctl disable rpi-tmon-mqtt.service
```

3. Stop the service if it is currently running:

```bash
    sudo systemctl stop rpi-tmon-mqtt.service
```

4. Delete the service file:

```bash
sudo rm /etc/systemd/system/rpi-tmon-mqtt.service
```

5. Reload the systemd daemon to remove the deleted service:

```bash
sudo systemctl daemon-reload
```

6. Reboot the Linux machine to ensure that the service is no longer present.
