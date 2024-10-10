import csv

def remove_duplicates_from_csv(input_file, output_file):
    unique_lines = set()

    # Read the CSV file and collect unique lines
    with open(input_file, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Read the header if it exists
        unique_lines.add(tuple(header))  # Add header to set

        for row in csv_reader:
            unique_lines.add(tuple(row))  # Add each row as a tuple to the set

    # Write unique lines to a new CSV file
    with open(output_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in unique_lines:
            csv_writer.writerow(line)

if __name__ == "__main__":
    input_csv_file = 'input.csv'  # Replace with your input file name
    output_csv_file = 'output.csv'  # Replace with your desired output file name
    remove_duplicates_from_csv(input_csv_file, output_csv_file)
    print(f'Duplicates removed. Unique lines written to {output_csv_file}')
