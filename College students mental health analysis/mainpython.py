import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("projext (1).csv")

# Function to convert "Yes" and "No" to binary
def to_binary(d):
    return 1 if d == "Yes" else 0

# Rename columns
newnames = ["Timestamps", "Names", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

# Convert categorical columns to binary
df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)
df["Year"] = df["Year"].str[-1:]

# Add "Condition" column
has_smtn = [(1 if df.iloc[row, df.columns.get_loc("Depression")] == 1 or
                  df.iloc[row, df.columns.get_loc("Anxiety")] == 1 or
                  df.iloc[row, df.columns.get_loc("Panic Attacks")] == 1 else 0) for row in range(len(df.index))]
df["Condition"] = has_smtn

# Main menu
while True:
    print("\nMenu:")
    print("1. Display the dataset")
    print("2. Display the dataset with new column names")
    print("3. Display the count of missing values")
    print("4. Convert categorical columns to binary")
    print("5. Display the dataset after adding the 'Condition' column")
    print("6. Display statistics")
    print("7. Display condition by gender plot")
    print("0. Exit")

    choice = input("Enter your choice (0-7): ")
    if choice.isdigit():
        choice = int(choice)
        if 0 <= choice <= 7:
            if choice == 0:
                print("Exiting the program.")
                break
            elif choice == 1:
                print(df)
            elif choice == 2:
                print(df.rename(columns=newnames))
            elif choice == 3:
                print(df.isna().sum())
            elif choice == 4:
                print("Columns converted to binary and Year column updated.")
            elif choice == 5:
                print(df)
            elif choice == 6:
                if "Depression" in df.columns and "Anxiety" in df.columns and "Panic Attacks" in df.columns:
                    num_depressed = (df["Depression"] == 1).sum()
                    num_anxious = (df["Anxiety"] == 1).sum()
                    num_pa = (df["Panic Attacks"] == 1).sum()
                    num_treated = (df["Treated"] == 1).sum()
                    num_w_condition = (df["Condition"] == 1).sum()
                    num_wo_condition = (df["Condition"] == 0).sum()
                    print("Depressed: {}\nAnxious: {}\nHaving panic attacks: {}\nBeing treated: {}\nTotal people with a condition: {}\nTotal people without: {}"
                          .format(num_depressed, num_anxious, num_pa, num_treated, num_w_condition, num_wo_condition))
                else:
                    print("Depression, Anxiety, or Panic Attacks columns not found in the DataFrame.")
            elif choice == 7:
                if "Depression" in df.columns and "Anxiety" in df.columns and "Panic Attacks" in df.columns and "Gender" in df.columns:
                    labels = ['Depressed', 'Anxious', 'Having Panic \nAttacks',
                              'Depressed and \nAnxious', 'Depressed and Having \nPanic Attacks',
                              'Anxious and Having \nPanic Attacks', 'All Three']

                    gender_counts = {
                        "Male": [(df[(df["Gender"] == "Male") & (df["Depression"] == 1)].shape[0]),
                                 (df[(df["Gender"] == "Male") & (df["Anxiety"] == 1)].shape[0]),
                                 (df[(df["Gender"] == "Male") & (df["Panic Attacks"] == 1)].shape[0]),
                                 (df[(df["Gender"] == "Male") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                                 (df[(df["Gender"] == "Male") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                                 (df[(df["Gender"] == "Male") & (df["Anxiety"] == 1) & (df["Depression"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                                 (df[(df["Gender"] == "Male") & (df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)].shape[0])],

                        "Female": [(df[(df["Gender"] == "Female") & (df["Depression"] == 1)].shape[0]),
                                   (df[(df["Gender"] == "Female") & (df["Anxiety"] == 1)].shape[0]),
                                   (df[(df["Gender"] == "Female") & (df["Panic Attacks"] == 1)].shape[0]),
                                   (df[(df["Gender"] == "Female") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                                   (df[(df["Gender"] == "Female") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                                   (df[(df["Gender"] == "Female") & (df["Anxiety"] == 1) & (df["Depression"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                                   (df[(df["Gender"] == "Female") & (df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)].shape[0])]
                    }

                    gender_counts["Male"] = np.array(gender_counts["Male"]) / (df["Gender"] == "Male").sum() * 100
                    gender_counts["Female"] = np.array(gender_counts["Female"]) / (df["Gender"] == "Female").sum() * 100
                    fig, ax = plt.subplots(figsize=(10, 3))
                    bottom = np.zeros(7)

                    for gender, gender_count in gender_counts.items():
                        p = ax.bar(labels,
                                   gender_count,
                                   width=0.8,
                                   label=gender,
                                   bottom=bottom)
                        bottom += gender_count
                        ax.bar_label(container=p,
                                     label_type='center',
                                     fontsize=10)

                    ax.set_title("Condition by Gender", fontsize=20)
                    plt.xticks(fontsize=8, ha='right', rotation=20)
                    ax.legend()
                    plt.show()
                else:
                    print("Depression, Anxiety, Panic Attacks, or Gender columns not found in the DataFrame.")
        else:
            print("Invalid choice. Please enter a number between 0 and 7.")
    else:
        print("Invalid input. Please enter a number.")
        
