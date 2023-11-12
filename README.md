# BioVerse - Autonomous Virtual Biology Lab
This is the repository for BioVerse submitted for EF 2023 Bio x AI Hackathon


## Overview

BioVerse is an AI-powered virtual lab that simulates real-world biology research workflows through multi-agent conversations. Users can pose problems and receive guided assistance across literature discovery, experimental design, computational analysis, and results interpretation and paper writing.

The goal of BioVerse is to streamline and automate biology research through the coordination of specialised research agents. These agents cover various aspects of the experimental process, including:

1. Research Assistant - Helps with literature review, documentation, project coordination.
2. Experimental Biologist - Designs and discusses hands-on wet lab experiments and protocols.
3. Bioinformatician - Provides guidance on computational analysis and omics data workflows.
4. Image Analyst - Assists with processing and extracting insights from microscopy imaging data.

Additionally, the system facilitates continuous improvement by periodically gathering feedback from users.

BioVerse aims to provide end-to-end support from early stages of research through publication. Users can pose problems, discuss experimental directions with the agents, collect resultant data, and receive computational analysis guidance. The goal is an autonomous and accessible virtual lab supporting open-ended life science research workflows.


## Tech stack/Technical approach
Langchain
OpenAI
ChromaDB: text embeddings were stored in a Vector Database
Django

## Agents

### 1. Image Analysis Agent

- Responsible for analyzing images obtained during experiments.
- Utilizes advanced image processing techniques to extract relevant information.
- Generates detailed reports on image analysis results.

### 2. Experiment Generation Agent

- Creates experimental protocols based on specified parameters.
- Considers input from users and ensures protocols align with research objectives.
- Supports the generation of diverse and customizable experiments.

### 3. Experiment Execution Agent

- Executes experiments based on generated protocols.
- Coordinates with lab equipment and monitors real-time data acquisition.
- Ensures proper adherence to experimental timelines.

### 4. Information Retrieval Agent

- Retrieves and organizes experimental data from various sources.
- Provides a centralized repository for easy access to experiment results.
- Supports data querying and reporting functionalities.

### User Feedback Mechanism

- Periodically collects feedback from users to enhance system performance.
- Incorporates user suggestions to improve agent functionalities.
- Maintains a feedback loop to iteratively refine the overall user experience.



## Usage

1. **Configuration:**
   - Adjust agent parameters and configurations based on experimental requirements.

2. **Experiment Setup:**
   - Use the Experiment Generation Agent to create customized experimental protocols.

3. **Execution:**
   - Deploy the Experiment Execution Agent to carry out the experiments in the laboratory.

4. **Analysis:**
   - Leverage the Image Analysis Agent to process and analyze acquired experimental data.

5. **Data Retrieval:**
   - Utilize the Information Retrieval Agent to access and retrieve experiment results.

6. **Feedback:**
   - Provide feedback through the designated channels to improve system performance.

## Dependencies

- Python 3.x
- [Library Name 1](link_to_library_1)
- [Library Name 2](link_to_library_2)
- ...


## Summary
BioVerse is a project designed to streamline and automate biology experiments through the coordination of specialized research agents. These agents cover various aspects of the experimental process, including image analysis, experiment generation, execution, and information retrieval. Additionally, the system facilitates continuous improvement by periodically gathering feedback from users.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/biology-experiments-orchestrator.git
   cd biology-experiments-orchestrator

# Team Contributors and Acknowledgements
This repository was BioVerse submitted for the EF 2023 Bio x AI Hackathon. Thank you to Entrepreneur First for sponsoring the event. Team members: 

