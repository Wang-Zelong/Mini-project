import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import kruskal

class DataAnalysis:
    def __init__(self, data_inspection):
        self.data_inspection = data_inspection

    def select3(self):
        print('For ANOVA, following are the variables available')
        print('Variable' + '            ' +'Type')
        print('1. Valuation ($B)' +  '   ' + 'Ratio')
        print('2. Country' +  '           ' + 'Nominal')
        print('3. REGION' +  '           ' + 'Nominal')
        print('4. NUM' +  '              ' + 'Interval')
        while True:
            num1 = input('Enter a continuous (interval/ratio) variable: ')
            if num1 == '1':
                variable1 = 'Valuation ($B)'
                break
            elif num1 == '4':
                variable1 = 'NUM'
                break
            elif num1 == '2' or num1 == '3':
                print('The variable is invalid, please select again')
            else:
                print('Invalid input, please enter a number between 1 and 4')
        while True:
            num2 = input('Enter a categorical (ordinal/nominal) variable: ')
            if num2 == '2':
                variable2 = 'Country'
                break
            elif num2 == '3':
                variable2 = 'REGION'
                break
            elif num2 == '1' or num2 == '4':
                print('The variable is invalid, please select again')
            else:
                print('Invalid input, please enter a number between 1 and 4')
        print('Performing Kruskal-Wallis Test instead…')
        result = self.kruskal_wallis(variable1, variable2)
        if result:
            stat, p_value = result
            print(f"Kruskal-Wallis Statistic: {stat}")
            print(f"p-value: {p_value}")
            if p_value < 0.05:
                print('Result is statistically significant.')
                print('Therefore, your Null Hypothesis is rejected.')
                print('There is a statistically significant difference in the average ' + variable1 + ' across the categories of ' + variable2)
            else:
                print('Result is not statistically significant.')
                print('Therefore, your Null Hypothesis cannot be rejected.')
                print('There is no statistically significant difference in the average ' + variable1 + ' across the categories of ' + variable2)
        else:
            print("Kruskal-Wallis test could not be performed.")

    def qq_plot(self, variable1):
        data = self.data_inspection.data
        sm.qqplot(data[variable1], line='s')
        plt.title('QQ Plot')
        plt.xlabel('Theoretical Quantiles')
        plt.ylabel('Sample Quantiles')
        plt.show()

    def kruskal_wallis(self, variable1, variable2):
        data = self.data_inspection.data
        groups = data[variable2].unique()
        if len(groups) < 2:
            print("Not enough groups for Kruskal-Wallis test.")
            return None
        try:
            group_data = [
                data[data[variable2] == group][variable1].dropna().values
                for group in groups
                if data[data[variable2] == group][variable1].dropna().size > 0
            ]
            if any(len(group) == 0 for group in group_data):
                print("One or more groups have no data.")
                return None
            stat, p_value = kruskal(*group_data)
            return stat, p_value
        except Exception as e:
            print(f"An error occurred: {e}")
            return None