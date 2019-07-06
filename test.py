'''
 https://datascienceschool.net/view-notebook/c645d51f308b4047aa78e8b343a2e181/
'''


from statsmodels.tsa.statespace.kalman_filter import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt

model1 = KalmanFilter(k_endog=1, k_states=1,
                      transition=[[1]], selection=[[1]], state_cov=[[10]],
                      design=[[1]], obs_cov=[[100]])

np.random.seed(0)
y1, x1 = model1.simulate(100)

print(x1)
print(y1)

plt.plot(y1, 'r:', label="관측값")
plt.plot(x1, 'g-', label="상태값")
plt.legend()
plt.title("로컬레벨 모형의 시뮬레이션 ($\sigma_w^2 = 10$, $\sigma_v^2 = 100$)")
plt.show()