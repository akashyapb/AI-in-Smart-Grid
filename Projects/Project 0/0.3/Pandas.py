import pandas as pd

#Reading the file from the database repository
df = pd.read_csv("//Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/Project 0/0.3/PMU01_140701.csv")

# Filter rows based on the condition
subset = df.loc[df["VCLPM:Magnitude"] < 199000, ["Timestamp", "VALPM:Magnitude", "VBLPM:Magnitude", "VCLPM:Magnitude"]]

# Save the resulting subset to a CSV file to manually verify the correctness of the condition application
subset.to_csv("//Users/Kashyap/Documents/Files/Academics/Institutions/Masters(USA)/IIT/Spring 2024 Semester/ECE563 (AI for Smart Grid)/Project 0/0.3/opsubset.csv", index=False)

# Print the resulting subset
print(subset)


