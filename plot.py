import pandas as pd
import matplotlib.pyplot as plt

file_path = 'workouts.csv'
workouts_df = pd.read_csv(file_path)

workouts_df['date'] = pd.to_datetime(workouts_df['date'], format='%d/%m/%Y')

plt.figure(figsize=(10, 6))

line_styles = ['-', '--', '-.', ':']  # Different line styles
for i, exercise in enumerate(workouts_df['exercise'].unique()):
    exercise_data = workouts_df[workouts_df['exercise'] == exercise]
    plt.plot(exercise_data['date'], exercise_data['weight'], marker='o', linestyle=line_styles[i % len(line_styles)], label=exercise)

plt.title('Weights Over Time by Exercise')
plt.xlabel('Date')
plt.ylabel('Weight (kg)')
plt.xticks(rotation=45)

plt.legend(title="Exercise", loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
plt.tight_layout()

plt.show()