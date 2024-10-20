from Data_Inspection import DataInspection

def main():
    # 创建 DataInspection 类的实例
    di = DataInspection()
    # 调用数据检查模块的方法
    di.load_csv()
    di.data_cleaning()
    di.basic_information()
    di.select1()

if __name__ == "__main__":
    main()