# gesture-controlled-robot-ros2



## Overview

This project demonstrates a gesture-controlled robot in a simulation environment using Ignition Gazebo and ROS 2. An IMU (Inertial Measurement Unit) connected via Arduino Nano captures hand gestures to control the robot's movement in the simulation.The robot is controlled using hand gestures detected by the IMU sensor. The IMU is mounted on the user's hand and connected to the Arduino Nano, which sends orientation data (yaw and pitch) to the PC via USB. A Python script reads the data and sends velocity commands to control the robot in Ignition Gazebo through ROS 2.

🎥 [**Watch the Demonstration**](https://drive.google.com/file/d/1Emu8EpixYeHzUSP-oKnuVpvai1Fv_Ksk/view?usp=sharing)

## 🧩 Components Used

### 🔧 Hardware

- Arduino Nano  
- MPU6050 IMU Sensor  
- USB Cable  

### 💻 Software

- ROS 2 (e.g., Humble / Foxy)  
- Ignition Gazebo (e.g., Fortress / Edifice)  
- Python 3  
- Arduino IDE  

---

## 🚀 Setup Instructions

1. Clone the repo 
```
git clone https://github.com/nivednivu1997/gesture-controlled-robot-ros2.git
```
2. Install ignition Gazebo by following official Documentation
```
https://gazebosim.org/api/gazebo/6/install.html
```
3. Open ignition Gazebo and select default world
```
  ign gazebo
```
4. Setup Arduino and IMU and upload code from arduino ide
```
  https://maker.pro/arduino/tutorial/how-to-interface-arduino-and-the-mpu-6050-sensor
```
5. Run gazebo ros gazebo bridge
```
  ros2 run ros_gz_bridge parameter_bridge /model/tugbot/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

6. Run Python node
```
cd gesture-controlled-robot-ros2 && python3 imu_teleop.py
```
## ✅ Testing

1. **Tilt your hand forward** – Robot should move **forward**.  
2. **Tilt your hand backward** – Robot moves **backward**.  
3. **Tilt left/right** – Robot **turns accordingly**.

---

## 👤 Author

Developed by **[Nived Krishnan]**  
Feel free to contribute or open issues for improvements!


