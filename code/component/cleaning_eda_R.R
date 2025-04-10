library(tidyverse)

#before I start trying to model and visualize, I want to get a better idea of the data that I am working with
#in this file I will use R code to clean the data from the original CSV file and begin basic EDA

#load in original data file
file_loc = "C:/Users/power/Desktop/Classes/DATS4001/25-spring-KPower/data/Vaccination_Concerns__Issues__and_Motivators___RespVaxView___Data___Centers_for_Disease_Control_and_Prevention__cdc.gov__20250224.csv"
data = read.csv(file_loc)

#CLEANING

#standardize column names to snake case
data = rename(data, vaccine = Vaccine)
data = rename(data, indicator_group = Indicator_group)
data = rename(data, indicator_category = Indicator_category)
data = rename(data, estimate = Estimate)
data = rename(data, lower_ci = Lower_ci)
data = rename(data, upper_ci = Upper_ci)
data = rename(data, sample_size = Unweighted.Sample.Size)
data = rename(data, month_label = Month_label)
data = rename(data, dashboard_type = Dashboard_type)
data = rename(data, suppression_flag = Suppression_flag)

#notice that Month_label has inconsistent formatting -> change Mon-yr to Month Year
data$month_label[data$month_label == "Aug-24"] = "August 2024/September 2024"
data$month_label[data$month_label == "Sep-24"] = "August 2024/September 2024"
data$month_label[data$month_label == "October 2024"] = "October 2024/November 2024"
data$month_label[data$month_label == "November 2024"] = "October 2024/November 2024"
data$month_label[data$month_label == "December 2024"] = "December 2024/January 2025"
data$month_label[data$month_label == "January 2025"] = "December 2024/January 2025"

#notice that survey is bimonthly with only concerns/issues were surveyed in Aug and only motivators surveyed in Sep (etc)

#split Timeframe_survey into separate start_survey and end_survey columns with date format
data = separate(data, Timeframe_survey, into = c("start_survey", "end_survey"),sep="-")
data$start_survey = as.Date(data$start_survey, "%m/%d/%Y")
data$end_survey = as.Date(data$end_survey, "%m/%d/%Y")

#identify unique values for each relevant column to help understand the dataset
uniques = lapply(data[,c(1:5,10,13,14)],unique)

#reformat so that the data is sorted by date and groups
data = arrange(data, start_survey, demo_group, demo_category, vaccine)

write.csv(data, "C:/Users/power/Desktop/Classes/DATS4001/25-spring-KPower/data/cleaned_vaccine_sentiment_data.csv", row.names = FALSE)


#EXPLORATORY DATA ANALYSIS

#basic statistics
summary(data)

#create separate dataframes for each indicator/demo group
agedf = data[data$demo_group == "Age",]
racedf = data[data$demo_group == "Race and Ethnicity",]
urbandf = data[data$demo_group == "Urbanicity",]
coveragedf = data[data$demo_group == "Vaccination coverage and intent",]
insurancedf = data[data$demo_group == "Insurance status",]
overalldf = data[data$demo_group == "Overall",]

#two way anovas for each new df
anova_age = aov(estimate ~ demo_category + indicator_category, data = agedf)
summary(anova_age) #low p values here
anova_race = aov(estimate ~ demo_category + indicator_category, data = racedf)
summary(anova_race) #low p value for indicator but not for demo
anova_urban = aov(estimate ~ demo_category + indicator_category, data = urbandf)
summary(anova_urban) #low p values, especially for indicator
anova_coverage = aov(estimate ~ demo_category + indicator_category, data = coveragedf)
summary(anova_coverage) #low p values here
anova_insurance = aov(estimate ~ demo_category + indicator_category, data = insurancedf)
summary(anova_insurance) #low p values here
anova_overall = aov(estimate ~ indicator_category, data = overalldf)
summary(anova_overall) #low p value
#age, vax coverage/intent, and insurance status seem to give the most variance in estimate value
#should I be doing one way here? maybe repeat with separations of sentiment and vaccine types?

