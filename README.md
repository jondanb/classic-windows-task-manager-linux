
# Classic Windows Task Manager Linux

This is a project designed to remake the Windows 7 era task manager on Linux. 
This project was written and tested on both KDE 5 and KDE 6.

<a href="./screenshots/performance_tab.png">
    <img src="./screenshots/performance_tab.png" alt="Performance Tab" width="400">
</a>

## Requirements
### Insalling Dependencies on Ubuntu
Install the following packages
```
sudo apt update
sudo apt install \
  python3-pyqt5 \
  python3-pyqt5.qttools \
  python3-pyqtgraph \
  python3-psutil \
  python3-dbus \
  python3-gi \
  gir1.2-gtk-3.0 \
  gir1.2-accountsservice-1.0
  ```
  
### Installing Dependencies on Arch
```
sudo pacman -Sy
sudo pacman -S \
  python-pyqt5 \
  python-pyqtgraph \
  python-psutil \
  python-dbus \
  python-gobject
  qt5ct \
  kvantum-qt5
```

### Installing Dependencies with PiP
```
pip install --upgrade pip
pip install PyQt5 pyqtgraph psutil dbus-python PyGObject
```

## Running the Program
First, clone the repository, and then run the main file.
```bash
git clone https://github.com/JonDanB/classic-windows-task-manager-linux.git
cd classic-windows-task-manager-linux
python3 main.py
```

## Screenshots
<p align="center">
  <a href="./screenshots/applications_tab.png">
    <img src="./screenshots/applications_tab.png" alt="Applications Tab" width="200">
  </a>
  <a href="./screenshots/network_tab.png">
    <img src="./screenshots/network_tab.png" alt="Network Tab" width="200">
  </a>
  <a href="./screenshots/performance_tab.png">
    <img src="./screenshots/performance_tab.png" alt="Performance Tab" width="200">
  </a>
</p>

<p align="center">
  <a href="./screenshots/processes_tab.png">
    <img src="./screenshots/processes_tab.png" alt="Processes Tab" width="200">
  </a>
  <a href="./screenshots/services_tab.png">
    <img src="./screenshots/services_tab.png" alt="Services Tab" width="200">
  </a>
</p>

