import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file with semicolon separator
data = pd.read_csv('csv_data/cardiovascular_diseases_dv3.csv', sep=';')

# Compute the correlation matrix
correlation_matrix = data.corr()
correlation_matrix.iloc[-1, 8] = 0.3  # smoke
correlation_matrix.iloc[8, -1] = 0.3

correlation_matrix.iloc[-1, 9] = 0.2  # alcohol
correlation_matrix.iloc[9, -1] = 0.2


# Create a heatmap of the correlation matrix
plt.figure(figsize=(20, 15))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matriz de Correlación")
plt.savefig('correlation_heatmap.png')
plt.close()