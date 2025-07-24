import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

class DataDashboard:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    def preview_data(self, rows=5):
        """Print a preview of the dataset"""
        print(self.df.head(rows))

    def summary_statistics(self):
        """Print summary statistics"""
        print(self.df.describe(include='all'))

    def plot_histogram(self, column):
        """Plot a histogram for a numeric column"""
        if column in self.numeric_cols:
            fig = px.histogram(self.df, x=column, nbins=20, title=f"Histogram of {column}")
            fig.show()
        else:
            print(f"❌ '{column}' is not a numeric column.")

    def plot_pie_chart(self, column):
        """Plot a pie chart for a categorical column"""
        if column in self.categorical_cols:
            fig = px.pie(self.df, names=column, title=f"Pie Chart of {column}")
            fig.show()
        else:
            print(f"❌ '{column}' is not a categorical column.")

    def plot_scatter(self, x_col, y_col, color_col=None):
        """Plot a scatter plot"""
        if x_col in self.numeric_cols and y_col in self.numeric_cols:
            fig = px.scatter(self.df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
            fig.show()
        else:
            print(f"❌ Both '{x_col}' and '{y_col}' must be numeric columns.")

    def plot_box_plot(self, x_col, y_col):
        """Plot a box plot"""
        if x_col in self.categorical_cols and y_col in self.numeric_cols:
            fig = px.box(self.df, x=x_col, y=y_col, title=f"Box Plot: {y_col} by {x_col}")
            fig.show()
        else:
            print(f"❌ '{x_col}' must be categorical and '{y_col}' must be numeric.")

    def plot_correlation_heatmap(self):
        """Plot a correlation heatmap for numeric columns"""
        corr = self.df[self.numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        plt.title("Correlation Heatmap")
        plt.show()

# -------------------------- MAIN CONSOLE INTERFACE --------------------------

def main():
    filepath = input("📂 Enter the path to your CSV file: ").strip()
    
    try:
        dashboard = DataDashboard(filepath)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return

    print("\n✅ File loaded successfully!")
    print("\n🧾 Preview of data:")
    dashboard.preview_data()

    print("\n📈 Summary statistics:")
    dashboard.summary_statistics()

    print("\nAvailable numeric columns:", dashboard.numeric_cols)
    print("Available categorical columns:", dashboard.categorical_cols)

    while True:
        print("\nChoose a plot:")
        print("1. Histogram")
        print("2. Pie Chart")
        print("3. Scatter Plot")
        print("4. Box Plot")
        print("5. Correlation Heatmap")
        print("6. Exit")
        choice = input("Enter choice number: ").strip()

        if choice == '1':
            col = input("Enter column name for Histogram: ").strip()
            dashboard.plot_histogram(col)

        elif choice == '2':
            col = input("Enter column name for Pie Chart: ").strip()
            dashboard.plot_pie_chart(col)

        elif choice == '3':
            x_col = input("Enter X-axis column: ").strip()
            y_col = input("Enter Y-axis column: ").strip()
            color_col = input("Enter color column (optional, press Enter to skip): ").strip()
            color_col = color_col if color_col else None
            dashboard.plot_scatter(x_col, y_col, color_col)

        elif choice == '4':
            x_col = input("Enter X-axis (categorical) column: ").strip()
            y_col = input("Enter Y-axis (numeric) column: ").strip()
            dashboard.plot_box_plot(x_col, y_col)

        elif choice == '5':
            dashboard.plot_correlation_heatmap()

        elif choice == '6':
            print("👋 Exiting Dashboard...")
            break

        else:
            print("❗ Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()

