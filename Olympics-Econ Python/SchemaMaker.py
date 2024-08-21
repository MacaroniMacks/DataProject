years = range(1960, 2024)  # 1960 to 2023 inclusive

schema_text = []

for year in years:
    schema_entry = {
        "name": year,
        "type": "FLOAT",
        "mode": "nullable"
    }
    schema_text.append(schema_entry)

# Print schema text with commas
for entry in schema_text:
    print(f"{entry},")