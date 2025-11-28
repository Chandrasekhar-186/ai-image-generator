Model Management and Configuration
This directory serves as the dedicated repository for all Generative AI model files utilized by the Image Generator application. This document provides formal guidance on the acquisition, integration, and essential configuration of compatible models.

 Model Acquisition Protocol
The application is engineered to utilize models compatible with established frameworks, such as the Hugging Face Diffusers library or standard Stable Diffusion checkpoints.

Sourcing Models
Users are instructed to acquire model assets from verified, trustworthy sources. Recommended starting points include:

Stable Diffusion v1.5: https://huggingface.co/runwayml/stable-diffusion-v1-5

Stable Diffusion XL (SDXL): https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

Integration
Model files, including associated configuration and weight files (e.g., .bin, .safetensors, config.json), must be placed within a dedicated subdirectory inside the models/ folder.

Example of the Required Directory Structure:

models/
└─ stable-diffusion-v1-5/
   ├─ config.json
   ├─ model_index.json
   ├─ scheduler/
   ├─ tokenizer/
   └─ diffusion_pytorch_model.bin
 System Configuration Requirements
To ensure the application detects and utilizes the integrated model correctly, the following configuration steps are mandatory:

Configuration File Update: The core application settings are managed in app/config.py. The designated model path variable within this file must be updated to precisely reflect the subdirectory name (e.g., 'stable-diffusion-v1-5').

Resource Allocation: Verification of adequate system resources, specifically GPU Video RAM (VRAM), is crucial. The resource requirements scale with the complexity of the chosen model. Failure to meet these requirements may lead to execution errors or significant performance degradation.

 Performance and Resource Considerations
Model Scaling: Models with higher complexity (e.g., SDXL) typically yield superior image fidelity and resolution but impose significantly greater demands on computational resources (GPU, memory, and processing time).

Experimentation: The modular pipeline design facilitates experimentation. Users can swap between different model architectures by integrating a new model directory and updating the path in app/config.py