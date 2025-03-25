# 🎾 ATP Tennis Data Processor (2000-2025)

This project downloads, processes, and organizes ATP tennis match data from 2000 to 2025 for analysis.

## 📋 About the Project

The ATP Tennis Data Processor automatically collects ATP men's tennis match results, organizing them into a consistent and clean format for statistical analysis and research.

## 🔧 Requirements

- Python 3.6 or higher
- Internet connection to download the data
- Dependencies listed in `requirements.txt`:
  - pandas
  - numpy
  - requests
  - openpyxl
  - xlrd
  - tqdm

## 🚀 How to Use

### Method 1: Direct Execution

1. **Clone or download this repository**

2. **Run the main script**:
   ```
   python ATP_Tennis_2000_2025.py
   ```

3. **Monitor the progress**:
   - The script will display a progress bar while downloading and processing the data
   - Upon completion, an `atp_tennis.csv` file will be created in the current directory

### Method 2: Dependency Verification

1. **First run the dependency checker**:
   ```
   python dependencies.py
   ```

2. **Then run the main script**:
   ```
   python ATP_Tennis_2000_2025.py
   ```

## 📊 Processed Data

The final `atp_tennis.csv` file contains the following columns:

- `Tournament` - Tournament name
- `Date` - Match date
- `Series` - Tournament category
- `Court` - Court type (indoor/outdoor)
- `Surface` - Playing surface (clay, grass, hard, carpet)
- `Round` - Tournament round
- `Best of` - Match format (3 or 5 sets)
- `Player_1` and `Player_2` - Player names
- `Winner` - Match winner
- `Rank_1` and `Rank_2` - Player rankings
- `Pts_1` and `Pts_2` - Player ranking points
- `Odd_1` and `Odd_2` - Player odds
- `Score` - Match score

## 🔄 Data Processing Workflow

1. ⬇️ **Downloading data** from multiple sources (2000-2025)
2. 🧹 **Data cleaning**:
   - Removing incomplete matches
   - Handling missing values
   - Normalizing formats
3. 🔄 **Standardization**:
   - Organizing data in player_1 vs player_2 format
   - Alternating winner/loser to avoid bias
4. 💾 **Exporting** to CSV

## ⚠️ Notes

- The script requires an internet connection to download the data
- The complete processing may take a few minutes
- Make sure you have enough disk space (~50MB)

## 📈 Usage Example

```python
import pandas as pd

# Load the processed data
tennis_data = pd.read_csv('atp_tennis.csv')

# View the first rows
print(tennis_data.head())

# Basic statistics
print(tennis_data.describe())
```

## 🤝 Contributions

Contributions are welcome! Feel free to open issues or submit pull requests with improvements.