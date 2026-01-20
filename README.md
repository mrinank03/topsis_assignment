# TOPSIS Package

🌐 **Live Demo:** [https://topsis-mrinank.streamlit.app/](https://topsis-mrinank.streamlit.app/)

## Project description

### TOPSIS Implementation

#### Overview

This Python package provides a straightforward implementation of the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) method for multi-criteria decision-making. With this tool, you can rank alternatives based on multiple criteria using weights and impacts for each criterion.

#### Features

* Easy-to-use command-line interface.
* Supports customizable weights and impacts for criteria.
* Outputs a ranked list of alternatives with TOPSIS scores.
* Handles CSV input and output for seamless integration with data workflows.

#### Usage

##### Web Interface (Recommended)

To use the interactive Streamlit web interface:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

**Features:**
- Upload CSV files with drag-and-drop
- Download sample CSV files
- Input weights and impacts interactively
- View results in a formatted table
- Send results via email (optional)
- Download results as CSV

##### Command-Line Interface

To execute TOPSIS, use the following command:

```
python topsis.py <input_file> <weights> <impacts> <output_file>
```

##### Arguments

* `<input_file>`: Path to the CSV file containing the input data. The first column should contain alternative names, and subsequent columns should contain numerical criteria values.
* `<weights>`: Comma-separated weights for each criterion (e.g., 1,2,3).
* `<impacts>`: Comma-separated impacts for each criterion (+ for benefit criteria, - for cost criteria, e.g., +, +, -, +).
* `<output_file>`: Path to the CSV file where the results will be saved.

##### Example

Suppose you have the following input file (`data.csv`):

| Alternative | Criterion 1 | Criterion 2 | Criterion 3 |
|-------------|-------------|-------------|-------------|
| A1          | 250         | 16          | 12          |
| A2          | 200         | 20          | 8           |
| A3          | 300         | 12          | 15          |
| A4          | 275         | 14          | 10          |

To rank the alternatives with weights `1,1,1` and impacts `+,+,-`, run:

```
python topsis.py data.csv 1,1,1 +,+,- results.csv
```

The output (`results.csv`) will include the TOPSIS scores and ranks:

| Alternative | Criterion 1 | Criterion 2 | Criterion 3 | Topsis Score | Rank |
|-------------|-------------|-------------|-------------|--------------|------|
| A1          | 250         | 16          | 12          | 0.6547       | 2    |
| A2          | 200         | 20          | 8           | 0.3001       | 4    |
| A3          | 300         | 12          | 15          | 0.8234       | 1    |
| A4          | 275         | 14          | 10          | 0.4921       | 3    |

##### Input File Requirements

* The input file must be a CSV with at least three columns.
* The first column should contain the names of the alternatives.
* The remaining columns should contain numerical values for criteria.

##### Output File

The output file will contain the original data along with two additional columns:

* `Topsis Score`: The calculated TOPSIS score for each alternative.
* `Rank`: The rank of each alternative based on the TOPSIS score (1 = best).

## Email Configuration

To enable email functionality in the Streamlit app:

1. **For Gmail:**
   - Enable 2-Factor Authentication on your Google Account
   - Generate an App Password: https://myaccount.google.com/apppasswords
   - Copy the generated password

2. **Configure .env file:**
   - Copy `.env.example` to `.env`
   - Update with your email and app password:
   ```
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password_here
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

3. **For other email providers:**
   - Outlook: smtp-mail.outlook.com, port 587
   - Yahoo: smtp.mail.yahoo.com, port 587

## Error Handling

The package validates inputs and raises errors for:

* Input files with fewer than three columns.
* Mismatched lengths of weights or impacts compared to the criteria.
* Invalid impact values (must be + or -).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Contact

For questions or feedback, please contact [mrinankjit@gmail.com](mailto:mrinankjit@gmail.com).