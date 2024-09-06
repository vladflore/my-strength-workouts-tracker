import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors

from pyscript import display, document
from pyodide.ffi import create_proxy

working_element = document.querySelector("#working")
start_date_element = document.querySelector("#start-date")
end_date_element = document.querySelector("#end-date")
exercises_element = document.querySelector("#exercises")

file_path = "workouts.csv"
workouts_df = pd.read_csv(file_path)

workouts_df["date"] = pd.to_datetime(workouts_df["date"], format="%d/%m/%Y")

start_date = workouts_df["date"].min()
end_date = workouts_df["date"].max()
start_date_formatted = start_date.strftime("%d/%m/%Y")
end_date_formatted = end_date.strftime("%d/%m/%Y")
start_date_element.innerHTML = f"Start Tracking Date: {start_date_formatted}"
end_date_element.innerHTML = f"End Tracking Date: {end_date_formatted}"

plt.figure(figsize=(15, 10))

color_maps = ["tab20", "Set3", "Paired"]
colors = []

for cmap_name in color_maps:
    cmap = plt.get_cmap(cmap_name)
    colors.extend([cmap(i) for i in range(cmap.N)])

colors = colors[:50]

unique_exercises = workouts_df["exercise"].unique()
dropdown = document.createElement("select")
default_option = document.createElement("option")
default_option.textContent = "Select an exercise"
default_option.value = ""
dropdown.appendChild(default_option)
for exercise in sorted(unique_exercises):
    option = document.createElement("option")
    option.textContent = exercise
    option.value = exercise
    dropdown.appendChild(option)


def on_dropdown_change(event):
    selected_exercise = dropdown.value
    plot_selected_exercise(selected_exercise)


proxy_callback = create_proxy(on_dropdown_change)
dropdown.addEventListener("change", proxy_callback)

exercises_element.appendChild(dropdown)

num_exercises = workouts_df["exercise"].nunique()
if num_exercises > len(colors):
    raise ValueError(
        f"Not enough colors! You have {len(colors)}, but need {num_exercises}."
    )

line_style = "-"

exercise_data_list = []

for i, exercise in enumerate(unique_exercises):
    exercise_data = workouts_df[workouts_df["exercise"] == exercise]
    exercise_data_list.append((exercise, exercise_data, colors[i]))

exercise_data_list.sort(key=lambda x: x[0])

for i, (exercise, exercise_data, color) in enumerate(exercise_data_list):
    plt.plot(
        exercise_data["date"],
        exercise_data["weight"],
        marker="o",
        linestyle=line_style,
        color=color,
        label=f"{i+1}. {exercise}",
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

plt.gca().axes.get_xaxis().set_visible(False)

plt.legend(
    title=f"Exercise (Total: {num_exercises})",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    ncol=1,
)
plt.tight_layout()

working_element.style.display = "none"
display(plt, target="mpl")


def plot_selected_exercise(selected_exercise):
    if not selected_exercise:
        return

    plt.clf()

    plt.figure(figsize=(15, 5))  # Smaller figure for the single exercise plot

    # Filter the data for the selected exercise
    exercise_data = workouts_df[workouts_df["exercise"] == selected_exercise]

    # Plot the data for the selected exercise
    plt.plot(
        exercise_data["date"],
        exercise_data["weight"],
        marker="o",
        linestyle="-",
        color="blue",  # You can change this color if desired
        label=selected_exercise,
    )

    # Add text annotations for each point
    for j in range(len(exercise_data)):
        plt.text(
            exercise_data["date"].iloc[j],
            exercise_data["weight"].iloc[j],
            f"{exercise_data['weight'].iloc[j]}",
            fontsize=8,
            ha="left",
            va="center",
        )

    # Set plot title and labels
    plt.title(f"Weight Progression for {selected_exercise}")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.gca().axes.get_xaxis().set_visible(True)  # Show x-axis for this plot

    # Add the legend
    plt.legend(loc="upper right")
    plt.tight_layout()

    # Display the plot below the main plot
    display(plt, target="mpl2")  # Use a different target area for this plot
