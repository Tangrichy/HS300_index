# 沪深300指数择时

`HS300_data_updated.xlsx`: 数据
​		`Sheet1`: 估值因子(PE, PB, Roverrt)
​		`Shee2`: 拥挤度因子 (Var, Corr)

`Evaluation.py`: 价值因子
`Crowding.py`: 拥挤度因子

**回测**

1. PBPE

   ![](./plot/back_test_pbpe.png)

2. Roverrt

   ![](./plot/back_test_roverrt.png)

3. PBPE and Roverrt 并集

   ![](./plot/back_test_pbpe_roverrt.png)