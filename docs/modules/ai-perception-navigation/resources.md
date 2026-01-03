---
sidebar_label: 'Resources'
sidebar_position: 3
---

# AI Perception & Navigation Resources

This page contains additional resources to support your learning of AI perception and navigation concepts.

## Core ROS 2 Navigation Packages

### Navigation 2 (Nav2)
- [Nav2 Documentation](https://navigation.ros.org/)
- [Nav2 GitHub Repository](https://github.com/ros-planning/navigation2)
- [Nav2 Tutorials](https://navigation.ros.org/tutorials/)

### Common Perception Packages
- `vision_opencv`: OpenCV integration with ROS 2
- `image_transport`: Efficient image transport
- `cv_bridge`: Converting between ROS and OpenCV formats
- `image_pipeline`: Collection of image processing tools
- `vision_msgs`: Standard messages for computer vision

### SLAM Packages
- `slam_toolbox`: Modern SLAM implementation
- `cartographer`: Google's SLAM library with ROS 2 support
- `rtabmap_ros`: Real-time appearance-based mapping
- `orb_slam3_ros2`: ORB-SLAM3 with ROS 2 integration

## Computer Vision Libraries

### OpenCV
- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [OpenCV GitHub](https://github.com/opencv/opencv)

### Deep Learning Frameworks
- [TensorFlow](https://www.tensorflow.org/)
- [PyTorch](https://pytorch.org/)
- [ROS 2 TensorFlow Integration](https://github.com/tier4/ros2_tensorflow)

### Specialized Libraries
- `PCL` (Point Cloud Library): 3D point cloud processing
- `Open3D`: 3D data processing library
- `scikit-image`: Image processing in Python

## SLAM Implementations

### Visual SLAM
- [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB-SLAM3)
- [LSD-SLAM](https://github.com/tum-vision/lsd_slam)
- [DVO-SLAM](https://github.com/tum-vision/dvo_slam)

### LiDAR SLAM
- [LOAM](https://github.com/laboshinl/loam_velodyne)
- [LeGO-LOAM](https://github.com/RobustFieldAutonomyLab/LeGO-LOAM)
- [A-LOAM](https://github.com/HKUST-Aerial-Robotics/A-LOAM)

### Multi-Sensor SLAM
- [RTAB-Map](https://introlab.github.io/rtabmap/)
- [Cartographer](https://google-cartographer-ros.readthedocs.io/)

## Path Planning Libraries

### OMPL (Open Motion Planning Library)
- [OMPL Documentation](https://ompl.kavrakilab.org/)
- [OMPL ROS 2 Integration](https://github.com/ros-planning/moveit2/tree/main/moveit_planners/ompl)

### SBPL (Search-Based Planning Library)
- [SBPL GitHub](https://github.com/sbpl/sbpl)

### Custom Planning Frameworks
- [MoveIt](https://moveit.ros.org/) - Motion planning for manipulation
- [SBPL lattice planner](https://github.com/ros-planning/navigation_experimental)

## Deep Learning Models for Perception

### Object Detection
- [YOLOv8](https://github.com/ultralytics/ultralytics) - Real-time object detection
- [YOLOv5](https://github.com/ultralytics/yolov5) - Earlier version with good documentation
- [Detectron2](https://github.com/facebookresearch/detectron2) - Facebook's detection library
- [OpenVINO](https://docs.openvino.ai/) - Intel's optimized inference engine

### Semantic Segmentation
- [Segment Anything Model (SAM)](https://segment-anything.com/) - Meta's zero-shot segmentation
- [DeepLab](https://github.com/tensorflow/models/tree/master/research/deeplab) - Google's segmentation model
- [PSPNet](https://github.com/hszhao/PSPNet) - Pyramid Scene Parsing Network

### Pose Estimation
- [MediaPipe](https://google.github.io/mediapipe/) - Google's perception framework
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) - Multi-person pose estimation

## Perception Datasets

### General Vision Datasets
- [COCO Dataset](https://cocodataset.org/) - Object detection and segmentation
- [ImageNet](https://www.image-net.org/) - Image classification
- [KITTI Dataset](http://www.cvlibs.net/datasets/kitti/) - Autonomous driving scenarios
- [Cityscapes](https://www.cityscapes-dataset.com/) - Urban scene understanding

### Robotics-Specific Datasets
- [Robotics Datasets](https://roboticsdatasets.com/) - Centralized list
- [Matterport3D](https://niessner.github.io/Matterport/) - 3D indoor environments
- [ScanNet](http://www.scan-net.org/) - 3D scene understanding

## Navigation Algorithms

### Path Planning Algorithms
- [A* Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) - Heuristic pathfinding
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) - Optimal pathfinding
- [RRT (Rapidly-exploring Random Trees)](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree) - Sampling-based planning
- [Potential Fields](https://en.wikipedia.org/wiki/Potential_field_method) - Force-based navigation

### Local Navigation Algorithms
- [Dynamic Window Approach (DWA)](https://en.wikipedia.org/wiki/Dynamic_window_approach) - Velocity-based local planning
- [Trajectory Rollout](https://www.cs.cmu.edu/~motionplanning/reading/rl/RL-Chapter1.pdf) - Model-based local planning
- [TEB (Timed Elastic Band)](https://github.com/rst-tu-dortmund/teb_local_planner) - Optimization-based local planning

## Sensor Simulation

### Camera Simulation
- [Gazebo Camera Plugin](http://gazebosim.org/tutorials?tut=ros_gzplugins#Camera)
- [BlenderProc](https://github.com/DLR-RM/BlenderProc) - Photorealistic dataset generation
- [Unity Perception](https://github.com/Unity-Technologies/UnityPerception) - Unity-based simulation

### LiDAR Simulation
- [Gazebo Ray Plugin](http://gazebosim.org/tutorials?tut=ros_gzplugins#RaySensor)
- [SICK Tim551 Simulation](https://github.com/uos/sick_tim) - 2D LiDAR simulation

## AI/ML Frameworks for Robotics

### TensorFlow in Robotics
- [ROS 2 TensorFlow Integration](https://github.com/tier4/ros2_tensorflow)
- [TensorFlow Lite](https://www.tensorflow.org/lite) - For embedded systems
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving) - Model deployment

### PyTorch in Robotics
- [PyTorch ROS Integration](https://github.com/AtsushiSakai/pytorch_ros_examples)
- [TorchScript](https://pytorch.org/docs/stable/jit.html) - For model optimization

### Specialized Robotics AI
- [ROS 2 Inference Engine](https://github.com/intel/ros2_intel_movidius_ncs)
- [OpenVINO](https://docs.openvino.ai/) - Intel's inference optimization

## Performance and Optimization

### Real-time Processing
- [ROS 2 Real-time Guidelines](https://docs.ros.org/en/rolling/Concepts/About-Quality-of-Service-Settings.html)
- [Real-time Perception](https://www.cs.cmu.edu/~kiranb/papers/realtime-perception.pdf)
- [Embedded AI](https://arxiv.org/abs/2003.03275) - Efficient AI on edge devices

### GPU Acceleration
- [CUDA with ROS](https://github.com/dusty-nv/ros_deep_learning)
- [OpenCL for Computer Vision](https://github.com/opencv/opencv/tree/master/samples/opencl)
- [TensorRT](https://developer.nvidia.com/tensorrt) - NVIDIA's inference optimizer

## Safety and Certification

### Safety Standards
- [ISO 10218-1](https://www.iso.org/standard/45703.html) - Industrial robots safety
- [ISO 13482](https://www.iso.org/standard/45704.html) - Personal care robots safety
- [ROS Safety Working Group](https://github.com/ros-safety) - ROS safety initiatives

### Verification and Validation
- [Model-based Design](https://www.mathworks.com/discovery/model-based-design.html)
- [Formal Methods in Robotics](https://arxiv.org/abs/1707.06543)
- [Testing Frameworks](https://github.com/ros-planning/navigation2/tree/main/nav2_system_tests)

## Tutorials and Examples

### Basic Perception Tutorials
1. [ROS 2 Image Processing](https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python)
2. [OpenCV with ROS 2](https://github.com/ros-perception/vision_opencv)
3. [Camera Calibration](https://github.com/ros-perception/image_pipeline/tree/ros2/camera_calibration)

### SLAM Tutorials
1. [SLAM Toolbox Tutorial](https://github.com/SteveMacenski/slam_toolbox)
2. [Cartographer Tutorial](https://google-cartographer-ros.readthedocs.io/en/latest/)
3. [RTAB-Map Tutorial](https://github.com/introlab/rtabmap_ros)

### Navigation Tutorials
1. [Nav2 Bringup Tutorial](https://navigation.ros.org/setup_guides/index.html)
2. [Custom Controller Tutorial](https://navigation.ros.org/plugin_tutorials/index.html)
3. [Behavior Trees Tutorial](https://github.com/micoloretan/ROSCon2020_BT)

## Research Papers and Publications

### Key Papers on Perception
- "YOLO9000: Better, Faster, Stronger" - Real-time object detection
- "Mask R-CNN" - Instance segmentation
- "Deep Residual Learning for Image Recognition" - ResNet architecture

### Key Papers on Navigation
- "The Dynamic Window Approach to Collision Avoidance" - DWA algorithm
- "A Formal Basis for the heuristic Determination of Minimum Cost Paths" - A* algorithm
- "Real-Time Dense Visual SLAM" - Dense SLAM approaches

### Key Papers on SLAM
- "Simultaneous Localisation and Mapping (SLAM): Part I" - Foundational SLAM paper
- "ORB-SLAM: A Versatile and Accurate Monocular SLAM System" - ORB-SLAM
- "RTAB-Map as an Open-Source Lidar and Visual SLAM Library for Large-Scale and Long-Term Online Operation" - RTAB-Map

## Tools and Utilities

### Visualization Tools
- **RViz2**: ROS 2 visualization tool
- **PlotJuggler**: Time series data visualization
- **rqt_image_view**: Real-time image viewing
- **Blender**: 3D visualization and modeling

### Debugging Tools
- **ros2 bag**: Data recording and playback
- **ros2 topic**: Topic monitoring and publishing
- **ros2 service**: Service call debugging
- **ros2 action**: Action monitoring

### Performance Analysis
- **ros2 topic hz**: Message rate analysis
- **ros2 lifecycle**: Node lifecycle management
- **top/htop**: System resource monitoring
- **nvidia-smi**: GPU monitoring (if applicable)

## Community Resources

### Forums and Communities
- [ROS Answers](https://answers.ros.org/) - Q&A forum
- [ROS Discourse](https://discourse.ros.org/) - Community discussions
- [Robotics Stack Exchange](https://robotics.stackexchange.com/) - Robotics-focused Q&A
- [Computer Vision Stack Exchange](https://computer-vision.stackexchange.com/) - CV-focused Q&A

### Conferences and Journals
- **ICRA** (International Conference on Robotics and Automation)
- **IROS** (International Conference on Intelligent Robots and Systems)
- **RSS** (Robotics: Science and Systems)
- **CVPR** (Computer Vision and Pattern Recognition)

## Troubleshooting Common Issues

### Perception Issues
- **Poor Detection Accuracy**: Check lighting conditions, retrain models, adjust thresholds
- **Slow Processing**: Optimize algorithms, use GPU acceleration, reduce resolution
- **False Positives**: Adjust confidence thresholds, improve training data

### Navigation Issues
- **Oscillatory Behavior**: Tune controller parameters, adjust velocity limits
- **Failure to Reach Goal**: Check costmap inflation, planner tolerances
- **Collision**: Increase safety margins, improve sensor coverage

### SLAM Issues
- **Drift**: Improve sensor quality, add loop closure, use better features
- **Map Quality**: Adjust parameters, improve sensor calibration
- **Real-time Performance**: Optimize algorithms, reduce map resolution

## Learning Path

1. Start with basic ROS 2 perception tutorials
2. Practice with OpenCV and basic image processing
3. Implement simple object detection algorithms
4. Learn SLAM fundamentals and practice with simulation
5. Explore deep learning approaches for perception
6. Implement navigation stack with your robot
7. Apply to the capstone project

Remember to always consider the computational requirements and real-time constraints when implementing perception and navigation systems on actual robots. The key to success is balancing accuracy with performance while maintaining safety.