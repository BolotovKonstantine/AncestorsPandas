# Overview
I created this software to further my learning and expertise as a software engineer by conducting a detailed analysis of birth-related data. The dataset in use provides information about birth records, including dates of birth and additional metadata. You can find the original dataset in this repository. I collected this data by myself by indexing archive records. 

The primary goal for writing this software is to explore trends in the data—specifically related to the number of records per year and how many records belong to a certain subset. By visualizing and grouping records, I hope to gain valuable insight into the distribution and prevalence of births across different years.

For a more in-depth overview of the project, including a demonstration of the data analysis process and a walkthrough of the code in action, please see this brief video:

[Software Demo Video](http://youtube.link.goes.here)

# Installation

## Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

## Steps to Install

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AncestorsPandas.git
   cd AncestorsPandas
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. **Run the main script**
   ```bash
   python main.py
   ```

2. **Using the CLI interface**
   ```bash
   python -m ancestors_pandas.cli --help
   ```
   This will display available commands and options.

# Data Analysis Results
- The number of records in the dataset was grouped by year, revealing trends in how many births fall into each year.
- A subset of the data (specified by a particular field) was isolated and analyzed to determine how many of those records belong to the subset versus the entire dataset.
- Additionally, surnames were normalized and tallied to observe their frequency distribution across the dataset.

Through these analyses, I was able to:
1. Identify how many records existed for each year.
2. Determine how many of those records were in the specific subset.
3. Visualize the occurrence of surnames by their normalized spelling to better understand naming patterns.

# Development Environment
- I developed this project using Python in a professional IDE setup.
- Key tools and libraries include:
  - [Python 3.x](https://www.python.org/)   
  - [Pandas](https://pandas.pydata.org/): for data manipulation and analysis   
  - [Matplotlib](https://matplotlib.org/): for creating visualizations   

# Useful Websites
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/index.html)

# Future Work
- Expand data cleaning functionality to handle more missing and malformed data.
- Incorporate additional visualizations for deeper insights (e.g., pie charts, line graphs).
- Automate the generation of reports to share with collaborators.
