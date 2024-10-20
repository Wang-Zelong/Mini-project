import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

from Data_Analysis import DataAnalysis
from More_Data_Analysis import MoreDataAnalysis

class DataInspection:
    def __init__(self):
        self.data = None

    def load_csv(self):
        file_path = input("Please provide the file path to the dataset: ")
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return

    def data_cleaning(self):
        # 删除Company列中仅含有数字的行
        self.data = self.data[~self.data['Company'].str.match('^\d+$')]
        # 将Valuation ($B)列中的空白数据替换为NaN
        self.data['Valuation ($B)'] = self.data['Valuation ($B)'].replace('', np.nan)
        # 转换为数值类型，无法转换的变为NaN
        self.data['Valuation ($B)'] = pd.to_numeric(self.data['Valuation ($B)'], errors='coerce')
        # 筛选出大于0且小于等于140的值进行中位数计算
        valid_values = self.data['Valuation ($B)'][(self.data['Valuation ($B)'] > 0) & (self.data['Valuation ($B)'] <= 140)]
        if not valid_values.empty:
            median_val = valid_values.median()
        else:
            median_val = np.nan
        # 替换Valuation ($B)列中小于等于0或大于140或为空的值为中位数
        self.data['Valuation ($B)'] = self.data['Valuation ($B)'].apply(lambda x: median_val if pd.isna(x) or x <= 0 or x > 140 else x)

    def basic_information(self):
        # 初始化一个空的列表来存储统计信息
        stats_data = []
        # 对每一列进行处理
        for col in self.data.columns:
            if self.data[col].dtype == 'object':  # 非数值列
                stats_data.append({
                    'Variable': col,
                    'Type of data': 'Nominal',
                    'Mean / Median / Mode': 'NA',
                    'Kurtosis': 'NA',
                    'Skewness': 'NA',
                    'Normality': 'NA'  # 添加Normality列
                })
            else:  # 数值列
                mean_val = self.data[col].mean()
                median_val = self.data[col].median()
                mode_val = self.data[col].mode()[0] if not self.data[col].mode().empty else 'NA'
                mean_median_mode = f"Mean: {mean_val:.2f}, Median: {median_val:.2f}, Mode: {mode_val}"
                kurtosis_val = self.data[col].kurtosis()
                skewness_val = self.data[col].skew()
                stats_data.append({
                    'Variable': col,
                    'Type of data': 'Ratio' if mean_val / median_val > 1 else 'Interval',  # 根据均值和中位数判断数据类型
                    'Mean / Median / Mode': mean_median_mode,
                    'Kurtosis': f"{kurtosis_val:.2f}",
                    'Skewness': f"{skewness_val:.2f}",
                    'Normality': 'Normal' if abs(skewness_val) < 0.5 and abs(kurtosis_val - 3) < 0.5 else 'Not Normal'
                    # 简单的正态性判断
                })
        # 将统计信息转换为DataFrame
        stats_df = pd.DataFrame(stats_data)
        # 设置pandas显示参数以确保所有内容都能完整显示
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', 1000)
        # 打印统计数据
        print('Following are the variables in your dataset')
        print(stats_df)

    def select1(self):
        print('How do you want to analyze your data?')
        print('1. Plot variable distribution')
        print('2. Conduct ANOVA')
        print('3. Conduct t-Test')
        print('4. Conduct chi-Square')
        print('5. Conduct Regression')
        print('6. Conduct Sentiment Analysis')
        print('7. Quit')
        choose1 = input('Enter your choice: ')
        if choose1 == '1':
            self.select2()
        if choose1 == '2':
            data_analysis = DataAnalysis(self)  # 传递 self 给 DataAnalysis
            data_analysis.select3()
            self.select1()
        if choose1 == '3':
            data_analysis = MoreDataAnalysis(self)
            data_analysis.select4()
            self.select1()
        if choose1 == '4':
            data_analysis = MoreDataAnalysis(self)
            data_analysis.select5()
            self.select1()
        if choose1 == '5':
            data_analysis = MoreDataAnalysis(self)
            data_analysis.regression()
            self.select1()
        if choose1 == '6':
            print('Looking for text data in your dataset…')
            print('Sorry, your dataset does not have a suitable length text data.')
            print('Therefore, Sentiment Analysis is not possible.')
            print('Returning to previous menu…')
            self.select1()
        if choose1 == '7':
            print("Exiting program.")
            sys.exit(0)

    def select2(self):
        print('Following variables are available for plot distribution:')
        print('1. Valuation ($B)')
        print('2. Country')
        print('3. REGION')
        print('4. NUM')
        print('5. BACK')
        print('6. QUIT')
        choose2 = input('Enter your choice: ')
        if choose2 == '1':
            if self.data is not None and 'Valuation ($B)' in self.data.columns:
                plt.hist(self.data['Valuation ($B)'], bins=30, edgecolor='black')
                # 设置X轴标题
                plt.xlabel('Valuation ($B)')
                # 设置X轴刻度
                plt.xticks(np.arange(min(self.data['Valuation ($B)']), max(self.data['Valuation ($B)']) + 1, step=5), rotation=45)  # 旋转刻度标签以便它们不会重叠
                # 设置X轴范围
                plt.xlim(min(self.data['Valuation ($B)']) - 1, max(self.data['Valuation ($B)']) + 1)
                # 设置Y轴标题
                plt.ylabel('Frequency')
                # 设置图表标题
                plt.title('Histogram with Valuation ($B)')
                # 显示网格
                plt.grid(False)
                # 显示图表
                plt.show()

                plt.figure(figsize=(10, 6))  # 设置图形的大小
                plt.boxplot(self.data['Valuation ($B)'], vert=True, patch_artist=True)  # vert=True表示箱线图是垂直的
                plt.title('Valuation ($B) Distribution')  # 设置标题
                plt.ylabel('Valuation in Billions ($)')  # 设置Y轴标签
                # 显示图形
                plt.grid(True)  # 显示网格
                plt.show()
            else:
                print("Data is not loaded or 'Valuation ($B)' column does not exist.")
            self.select2()

        if choose2 == '2':
            country_counts = self.data['Country'].value_counts()
            plt.figure(figsize=(20, 10))
            # 创建条形图
            plt.bar(country_counts.index, country_counts.values, color='skyblue')  # 使用 skyblue 颜色绘制条形图
            # 设置图表标题和轴标签
            plt.title('Number of Companies by Country')  # 设置标题
            plt.xlabel('Country')  # 设置 X 轴标签
            plt.ylabel('Number of Companies')  # 设置 Y 轴标签
            # 设置 X 轴刻度标签，防止重叠
            plt.xticks(rotation=45)  # 将 X 轴刻度标签旋转 45 度
            # 显示图表
            plt.show()
            self.select2()

        if choose2 == '3':
            country_counts = self.data['REGION'].value_counts()
            plt.figure(figsize=(10, 6))
            # 创建条形图
            plt.bar(country_counts.index, country_counts.values, color='skyblue')  # 使用 skyblue 颜色绘制条形图
            # 设置图表标题和轴标签
            plt.title('Number of Companies by Region')  # 设置标题
            plt.xlabel('Region')  # 设置 X 轴标签
            plt.ylabel('Number of Companies')  # 设置 Y 轴标签
            # 设置 X 轴刻度标签，防止重叠
            plt.xticks(rotation=45)  # 将 X 轴刻度标签旋转 45 度
            # 显示图表
            plt.show()
            self.select2()

        if choose2 == '4':
            if self.data is not None and 'NUM' in self.data.columns:
                plt.hist(self.data['NUM'], bins=5, edgecolor='black')
                # 设置X轴标题
                plt.xlabel('NUM')
                # 设置X轴刻度
                plt.xticks(np.arange(min(self.data['NUM']), max(self.data['NUM']) + 1, step=1))  # 旋转刻度标签以便它们不会重叠
                # 设置X轴范围
                plt.xlim(min(self.data['NUM']), max(self.data['NUM']))
                # 设置Y轴标题
                plt.ylabel('Frequency')
                # 设置图表标题
                plt.title('Histogram with NUM')
                # 显示网格
                plt.grid(False)
                # 显示图表
                plt.show()
                self.select2()

        if choose2 == '5':
            print('Returning to previous menu…')
            self.select1()

        if choose2 == '6':
            print("Exiting program.")
            sys.exit(0)