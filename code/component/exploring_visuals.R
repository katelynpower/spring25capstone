library(plotly)
#Here I plan to create a few visualizations of my data to explore options for my final viz product
file_loc = "C:/Users/power/Desktop/Classes/DATS4001/25-spring-KPower/data/cleaned_vaccine_sentiment_data.csv"
data = read.csv(file_loc)

mat1 = arrange(data[data$demo_group=="Overall" & data$month_label=="December 2024/January 2025" & data$vaccine=="COVID-19",],indicator_category)

fig = plot_ly(mat1, x=~indicator_category, y=~estimate, type="bar")
fig = fig %>% layout(title = "likelihood of covid concern December 2024",
                         xaxis = list(title = "reasoning"),
                         yaxis = list(title = "percent"))
fig

fig = plot_ly(mat1, labels=~indicator_category, values=~estimate, type='pie')
fig

mat2 = data[data$demo_group=="Overall" & data$vaccine=="COVID-19" & data$indicator_category=="Do not trust government",]
fig = plot_ly(mat2, x=~month_label, y=~estimate, type='bar')
fig = fig %>% layout(title = "likelihood of covid vax affected by mistrust in gov", xaxis = list(title="month"),list(title="percent"))
fig

