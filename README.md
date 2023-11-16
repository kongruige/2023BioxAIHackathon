# BioVerse - Autonomous Virtual Biology Lab
Welcome to the GitHub repository for BioVerse, an innovative project that earned a 4th place finish at the EF 2023 Bio x AI Hackathon. BioVerse represents a groundbreaking step in combining artificial intelligence with biology research, offering a comprehensive virtual lab experience.

![Alt text](/images/logo.jpeg)

## Overview
BioVerse is an AI-powered virtual lab that simulates real-world biology research workflows through multi-agent conversations. Users can pose problems and receive guided assistance across literature discovery, experimental design, computational analysis, and results interpretation and paper writing. The goal of BioVerse is to streamline and automate biology research through the coordination of specialised research agents. These agents cover various aspects of the experimental process, including:

## Agents
1. Principal Investigator - Serves as the coordinating agent, and critiques the works of other agents to ensure high quality
2. Research Assistant - An agents which conducts literature review, documentation, project coordination.
2. Experimental Biologist - Designs and discusses hands-on wet lab experiments and protocols.
3. Bioinformatician - Provides guidance on computational analysis and omics data workflows.
4. Image Analyst - Assists with processing and extracting insights from microscopy imaging data.

Additionally, the system facilitates continuous improvement by periodically gathering feedback from users. BioVerse aims to provide end-to-end support from early stages of research through publication. Users can pose problems, discuss experimental directions with the agents, collect resultant data, and receive computational analysis guidance. The goal is an autonomous and accessible virtual lab supporting open-ended life science research workflows.

## Team
- [Ananya Bhalla](https://www.linkedin.com/in/ananyabhalla/) - Team Lead & Bio Scientist (The Francis Crick Institute & Kings College)
- [Kosi Asuzu](https://www.linkedin.com/in/kosi-asuzu-793494190/) - AI/ML Engineer (Birmingham City University & Ivy)
- [Ruige Kong](https://www.linkedin.com/in/ruige-kong-6685611a3/) - AI/ML Engineer (University of Cambridge & European  Bioinformatics Institute)
- [Oliver Hernandez](https://www.linkedin.com/in/oliverhdez/) - Bio Scientist (Imperial College)
- [Henry Ndubuaku](https://www.linkedin.com/in/henry-ndubuaku-7b6350b8/) - AI/NLP Scientist (Coconut Head)


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


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/biology-experiments-orchestrator.git
   cd biology-experiments-orchestrator```

2. Install: ```pip install requirements.txt```

3. Run: ```python3 main.py```