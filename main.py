import matplotlib.pyplot as plt
import pandas as pd

from pyscript import display, document


working_element = document.querySelector('#working')

file_path = "workouts.csv"
workouts_df = pd.read_csv(file_path)

workouts_df["date"] = pd.to_datetime(workouts_df["date"], format="%d/%m/%Y")

plt.figure(figsize=(15, 10))

line_styles = ["-", "--", "-.", ":"]
for i, exercise in enumerate(workouts_df["exercise"].unique()):
    exercise_data = workouts_df[workouts_df["exercise"] == exercise]
    plt.plot(
        exercise_data["date"],
        exercise_data["weight"],
        marker="o",
        linestyle=line_styles[i % len(line_styles)],
        label=exercise,
    )
    for j in range(len(exercise_data)):
        plt.text(
            exercise_data["date"].iloc[j],
            exercise_data["weight"].iloc[j],
            f"{exercise_data['weight'].iloc[j]}",
            fontsize=8,
            ha="left",
            va="center",
        )

plt.title("Weight Progression")
plt.xlabel("Date")
plt.ylabel("Weight (kg)")
plt.xticks(rotation=45)

plt.legend(title="Exercise", loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)
plt.tight_layout()

working_element.style.display = 'none'
display(plt, target="mpl")
