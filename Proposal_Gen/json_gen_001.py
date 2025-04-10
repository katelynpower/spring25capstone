#%%
import json
import os
import shutil

#%%

def save_to_json(data, output_file_path):
    with open(output_file_path, 'w') as output_file:
        json.dump(data, output_file, indent=2)

semester2code = { "sp":"01", "spr":"01", "spring":"01", "su":"02", "sum":"02", "summer":"02", "fa":"03", "fall":"03"}
thisfilename = os.path.basename(__file__) # should match _ver for version, ideally 3-digit string starting as "000", up to "999"

data_to_save = \
    {
        # -----------------------------------------------------------------------------------------------------------------------
        "Version":
            """001""",
        # -----------------------------------------------------------------------------------------------------------------------
        "Year":
            """2025""",
        # -----------------------------------------------------------------------------------------------------------------------
        "Semester":
            """Spring""",
        # -----------------------------------------------------------------------------------------------------------------------
        "project_name":
            """Predicting and Visualizing Vaccine Sentiment Across Demographics""",
        # -----------------------------------------------------------------------------------------------------------------------
        "Objective":
            """ 
            I plan to investigate and predict patterns in sentiments towards COVID, flu, and RSV vaccinations. I am interested in 
            learning how different demographics and types of vaccine may affect a person’s perspective and motivation to get 
            vaccinated over time. I would like to include both predictive and visualization elements in my project, such as 
            predicting the greatest motivators/concerns for vaccines in the future and highlighting patterns in the vaccination 
            motivators/concerns of certain demographics.
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Dataset":
            """
            This data comes from the CDC’s VaxView team and is published by National Center for Immunization and Respiratory 
            Diseases, which are reliable government organizations. The Footnotes also lists other aspects of reliability such as 
            methods of limiting bias. The datatypes are all either text or numerical. 
            The dataset is sourced from this website: https://data.cdc.gov/Vaccinations/Vaccination-Concerns-Issues-and-Motivators-RespVax/94wp-9pid/about_data 
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Rationale":
            """
            During the COVID-19 pandemic, the topic of vaccinations became highly political, likely affecting the overall impact 
            of the pandemic, suggesting that the public's motivation for getting a vaccine is crucial for maintaining the herd 
            immunity threshold and saving lives. I am interested in learning how different demographics and types of vaccine may 
            affect a person’s perspective and motivation to get vaccinated over time. The results of this project could be used to 
            assist public health organization in effectively targeting vaccine messaging to increase immunization rates in the US.
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Approach":
            """
            I plan on approaching this capstone through several steps.  

            1. Prepare data through cleaning and exploratory data analysis.
            2. Work on the covariate features importance.  
            3. Use covariate features to model vaccination sentiment with classical machine learning techniques.
            4. Synthesize my findings through the creation of a professional dashboard for data visualization.
            5. Culminate my work with a written report and poster.
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Timeline":
            """
            This a rough time line for this project:  

            - (2 Weeks) Data Cleaning and EDA  
            - (2 Weeks) Feature Importance 
            - (3 Weeks) Modeling  
            - (3 Weeks) Visualization
            - (1 Week) Writing Report  
            - (1 Week) Creating Poster and Finalizing Presentation 
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Expected Number Students":
            """
            This project will be done individually.  
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Possible Issues":
            """
            The dataset website is not very descriptive in terms of giving clear definitions of all terms. If necessary, I can 
            address this issue by contacting the team. Another challenge may rise due to the organization of the demographics 
            within the dataset.
.
            """,
        # -----------------------------------------------------------------------------------------------------------------------
        "Proposed by": "Katelyn Power",
        "Proposed by email": "kpower@gwu.edu",
        "instructor": "Sushovan Majhi",
        "instructor_email": "s.majhi@gwu.edu",
        "github_repo": "https://github.com/GW-datasci/25-spring-KPower",
        # -----------------------------------------------------------------------------------------------------------------------
    }
os.makedirs(
    os.getcwd() + f'{os.sep}Proposals{os.sep}{data_to_save["Year"]}{semester2code[data_to_save["Semester"].lower()]}{os.sep}{data_to_save["Version"]}',
    exist_ok=True)
output_file_path = os.getcwd() + f'{os.sep}Proposals{os.sep}{data_to_save["Year"]}{semester2code[data_to_save["Semester"].lower()]}{os.sep}{data_to_save["Version"]}{os.sep}'
save_to_json(data_to_save, output_file_path + "input.json")
shutil.copy(thisfilename, output_file_path)
print(f"Data saved to {output_file_path}")
