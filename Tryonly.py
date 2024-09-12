#Summary Statistics of Screen time by gender
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Load datasets
df1 = pd.read_csv('dataset1.csv')  # Demographic data
df2 = pd.read_csv('dataset2.csv')  # Screen time data

# Merge datasets on 'ID'
merged_df = pd.merge(df1, df2, on='ID')

# Calculate summary statistics by gender
summary_stats_gender = merged_df.groupby('gender')[['C_we', 'G_we', 'S_we', 'T_we', 'C_wk', 'G_wk', 'S_wk', 'T_wk']].agg(['mean', 'median', 'std'])

# Display the summary statistics
print(summary_stats_gender)

# Extract the mean values from summary_stats_gender
mean_screen_time = summary_stats_gender.xs('mean', level=1, axis=1)

####
# Create a bar chart for mean screen time by gender
#mean_screen_time.plot(kind='bar', figsize=(10, 6))
#plt.title('Mean Screen Time by Gender')
#plt.xlabel('Gender (0 = Female, 1 = Male)')
#plt.ylabel('Mean Hours')
#plt.xticks(rotation=0)
#plt.legend(title='Screen Time Activity')
#plt.show()

# Extract mean smartphone usage (S_we) by gender
#mean_smartphone_usage = mean_screen_time['S_we']

# Create a pie chart for smartphone usage by gender
#plt.figure(figsize=(6, 6))
#plt.pie(mean_smartphone_usage, labels=['Female', 'Male'], autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
#plt.title('Mean Smartphone Usage on Weekends (S_we) by Gender')
#plt.show()
#####

#Frequency distribution##########

# Load dataset3 
df3 = pd.read_csv('dataset3.csv')  # Well-being data

# Frequency distribution of well-being scores
wellbeing_distribution = df3[['Optm', 'Relx', 'Conf']].apply(pd.Series.value_counts)

# Display the frequency distribution
print(wellbeing_distribution)

# Plot bar chart for frequency distribution of well-being scores
#wellbeing_distribution.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'lightgreen', 'salmon'])
#plt.title('Frequency Distribution of Well-being Scores (Optm, Relx, Conf)')
#lt.xlabel('Well-being Score (1 = Low, 5 = High)')
#plt.ylabel('Number of Respondents')
#plt.xticks(rotation=0)
#plt.legend(title='Well-being Variables')
#plt.show()
######

# Extract frequency distribution for 'Optm' (optimism)
#optm_distribution = wellbeing_distribution['Optm']

# Plot pie chart for optimism score distribution
#plt.figure(figsize=(6, 6))
#plt.pie(optm_distribution, labels=optm_distribution.index, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen', 'salmon', 'yellow', 'pink'])
#plt.title('Distribution of Optimism Scores (Optm)')
#plt.axis('equal') 
#plt.show()
######

#t-test################

# Merge the well-being data with the previously merged demographic and screen time data
merged_df_full = pd.merge(merged_df, df3, on='ID')

# Frequency distribution of well-being scores
wellbeing_distribution = merged_df_full[['Optm', 'Relx', 'Conf']].apply(pd.Series.value_counts)

# Display the frequency distribution
print(wellbeing_distribution)

# Define high vs. low social media users based on median social media usage
median_social_media = merged_df_full['S_we'].median()
merged_df_full['social_media_group'] = ['High' if x > median_social_media else 'Low' for x in merged_df_full['S_we']]

# Perform t-test on optimism scores between high and low social media users
t_stat, p_value = ttest_ind(merged_df_full[merged_df_full['social_media_group'] == 'High']['Optm'],
                            merged_df_full[merged_df_full['social_media_group'] == 'Low']['Optm'])

# Display the t-test results and p-value
print(f"T-test results: t-statistic = {t_stat}, p-value = {p_value}")

# Calculate the number of users high vs. low social media users
#social_media_counts = merged_df_full['social_media_group'].value_counts()

# Create a pie chart of high vs. low social media users
#plt.figure(figsize=(6, 6))
#plt.pie(social_media_counts, labels=social_media_counts.index, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightblue'])
#plt.title('Distribution of High and Low Social Media Users')
#plt.axis('equal') 
#plt.show()

#ANOVA test###################

from scipy.stats import f_oneway

# Divide into (low, medium, high screen time users) in the merged_df_full DataFrame
merged_df_full['social_media_tertile'] = pd.qcut(merged_df_full['S_we'], 3, labels=["Low", "Medium", "High"])

# Perform ANOVA on optimism scores for the different social media users
anova_result = f_oneway(merged_df_full[merged_df_full['social_media_tertile'] == 'Low']['Optm'],
                       merged_df_full[merged_df_full['social_media_tertile'] == 'Medium']['Optm'],
                       merged_df_full[merged_df_full['social_media_tertile'] == 'High']['Optm'])

# Display the ANOVA results (f-stat and p-value)
print(f"ANOVA results: F-statistic = {anova_result.statistic}, p-value = {anova_result.pvalue}")

#####
# Calculate the mean optimism scores for each social media usage group (Low, Medium, High)
mean_optm_low = merged_df_full[merged_df_full['social_media_tertile'] == 'Low']['Optm'].mean()
mean_optm_medium = merged_df_full[merged_df_full['social_media_tertile'] == 'Medium']['Optm'].mean()
mean_optm_high = merged_df_full[merged_df_full['social_media_tertile'] == 'High']['Optm'].mean()

# Create a list of the means
means = [mean_optm_low, mean_optm_medium, mean_optm_high]

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(['Low Social Media Users', 'Medium Social Media Users', 'High Social Media Users'], means, color=['lightblue', 'lightgreen', 'lightcoral'])
plt.title('Mean Optimism Scores by Social Media Usage Group')
plt.xlabel('Social Media Usage Group')
plt.ylabel('Mean Optimism Score')
plt.xticks(rotation=0)
plt.show()
#####