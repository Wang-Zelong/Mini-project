import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class MoreDataAnalysis:
    def __init__(self, data_inspection):
        self.data_inspection = data_inspection

    def select0(self):
        print('For regression, following are the variables available')
        print('Variable' + '            ' + 'Type')
        print('1. Valuation ($B)' + '   ' + 'Ratio')
        print('2. Country' + '           ' + 'Nominal')
        print('3. REGION' + '           ' + 'Nominal')
        print('4. NUM' + '              ' + 'Interval')
        while True:
            num1 = input('Enter a variable（from 2 to 4: ')
            if num1 == '2':
                variable1 = 'Country'
                break
            elif num1 == '3':
                variable1 = 'REGION'
                break
            elif num1 == '4':
                variable1 = 'NUM'
                break
            else:
                print('Invalid input')

        while True:
            num2 = input('Enter a continuous (interval/ratio) variable(but not NUM): ')
            if num2 == '1':
                variable2 = 'Valuation ($B)'
                break
            else:
                print('Invalid input')

        print('Performing regression over the selected variables…')
        self.regression(variable1, variable2)

    def regression(self, variable1, variable2):
        data = self.data_inspection.data
        print(f'Performing regression with {variable1} and {variable2}')

        if variable1 == 'Country':
            x = data[variable1].astype('category').cat.codes
        elif variable1 == 'REGION':
            x = data[variable1].astype('category').cat.codes
        elif variable1 == 'NUM':
            x = data[variable1]
        else:
            print("Invalid categorical variable selected")
            return

        if variable2 == 'Valuation ($B)':
            y = data[variable2].astype(float)
        else:
            print("Invalid continuous variable selected")
            return

        if not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number):
            print("One of the variables is not numeric")
            return

        # 使用有效的数据点进行线性回归
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        plt.scatter(x, y, label='Data points')
        plt.plot(x, intercept + slope * x, 'r', label='Fitted line')
        plt.xlabel(variable1)
        plt.ylabel(variable2)
        plt.title(f'Regression: {variable1} vs {variable2}')
        plt.legend()
        plt.show()

        print('Slope:', slope)
        print('Intercept:', intercept)
        print('R-squared:', r_value ** 2)  # R-squared is the square of r_value
        print('P-value:', p_value)
        print('Standard Deviation:', std_err)

    def select4(self):
        print('For t-test, following are the variables available')
        print('Variable' + '            ' +'Type')
        print('1. Valuation ($B)' +  '   ' + 'Ratio')
        print('2. Country' +  '           ' + 'Nominal')
        print('3. REGION' +  '           ' + 'Nominal')
        print('4. NUM' +  '              ' + 'Interval')
        while True:
            num1 = input('Enter a continuous (interval/ratio) variable: ')
            if num1 == '1':
                variable1 = 'Valuation ($B)'
                break  # 如果输入正确，则退出循环
            elif num1 == '4':
                variable1 = 'NUM'
                break  # 如果输入正确，则退出循环
            elif num1 == '2' or num1 == '3':
                print('The variable is invalid, please select again')
                # 如果输入无效，继续循环，不退出
            else:
                print('Invalid input, please enter a number between 1 and 4')
                # 如果输入不是1到4之间的数字，提示用户并继续循环
        while True:
            num2 = input('Enter a categorical (ordinal/nominal) variable: ')
            if num2 == '2':
                variable2 = 'Country'
                break  # 如果输入正确，则退出循环
            elif num2 == '3':
                variable2 = 'REGION'
                break  # 如果输入正确，则退出循环
            elif num2 == '1' or num2 == '4':
                print('The variable is invalid, please select again')
                # 如果输入无效，继续循环，不退出
            else:
                print('Invalid input, please enter a number between 1 and 4')
                # 如果输入不是1到4之间的数字，提示用户并继续循环
        print('Performing t-test over the selected variables…')
        self.t_test(variable1, variable2)

    def t_test(self, variable1, variable2):
        data = self.data_inspection.data
        groups = data[variable2].unique()
        if len(groups) < 2:
            print("Not enough groups for t-test.")
            return
        group_data = [
            data[data[variable2] == group][variable1].dropna().values
            for group in groups if data[data[variable2] == group][variable1].dropna().size > 0
        ]
        if any(len(group) == 0 for group in group_data):
            print("One or more groups have no data.")
            return
        if len(group_data) < 2:
            print("Not enough groups for t-test.")
            return
        # Check if all values in a group are identical
        identical_groups = [group for group in group_data if np.all(group == group[0])]
        if len(identical_groups) == len(group_data):
            print("Warning: All groups have identical values.")
            return
        # Perform t-test only if there are groups with varying data
        varying_groups = [group for group in group_data if not np.all(group == group[0])]
        if len(varying_groups) < 2:
            print("Not enough groups with varying data for t-test.")
            return
        t_stat, p_value = stats.ttest_ind(varying_groups[0], varying_groups[1], nan_policy='omit')
        print(f"T-statistic: {t_stat}, P-value: {p_value}")

    def select5(self):
        print('For chi-square-test, following are the variables available')
        print('Variable' + '            ' + 'Type')
        print('1. Company' + '         ' + 'Nominal')
        print('2. Country' + '         ' + 'Nominal')
        print('3. REGION' + '          ' + 'Nominal')
        print('4. Industry' + '        ' + 'Nominal')
        variable3 = None  # 初始化 variable3
        variable4 = None  # 初始化 variable4
        while variable3 is None:  # 确保 variable3 被赋值
            num1 = input('Enter a variable (Country or REGION): ')
            if num1 == '2':
                variable3 = 'Country'
            elif num1 == '3':
                variable3 = 'REGION'
            elif num1 in ['1', '4']:
                print('The variable is invalid, please select again')
            else:
                print('Invalid input, please enter a number between 1 and 4')
        while variable4 is None:  # 确保 variable4 被赋值
            num2 = input('Enter a variable (Industry or Company): ')
            if num2 == '1':
                variable4 = 'Industry'
            elif num2 == '4':
                variable4 = 'Company'
            elif num2 in ['2', '3']:
                print('The variable is invalid, please select again')
            else:
                print('Invalid input, please enter a number between 1 and 4')
        print('Performing chi-square-test over the selected variables…')
        self.chi_square_test(variable3, variable4)

    def chi_square_test(self, variable3, variable4):
        data = self.data_inspection.data  # 确保使用正确的数据源
        # 创建一个列联表（contingency table）
        contingency_table = pd.crosstab(data[variable3], data[variable4])
        # 执行卡方检验
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        # 设置显著性水平，例如0.05
        significance_level = 0.05
        # 获取卡方分布的临界值
        critical_value = stats.chi2.ppf(1 - significance_level, dof)
        # 打印卡方统计量、P值和自由度
        print(f"Chi-squared statistic: {chi2_stat}, P-value: {p_value}, Degrees of freedom: {dof}")
        # 判断两个变量是否有关系的代码
        if p_value < significance_level:
            print("Reject the null hypothesis: There is a significant relationship between the two variables.")
        else:
            print("Fail to reject the null hypothesis: There is no significant relationship between the two variables.")
