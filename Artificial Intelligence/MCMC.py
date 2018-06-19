import pymc as pm
import numpy as np
import pandas as pd

values = [1.]
length = len(values)

rain = pm.Bernoulli('rain', 0.2, value=np.ones(length))

p_class_late = pm.Lambda('p_class_late', lambda rain=rain: np.where(rain, 0.9, 0.5))
class_late = pm.Bernoulli('class_late', p_class_late, value=np.ones(length))

p_traffic = pm.Lambda('p_traffic', lambda class_late=class_late, rain=rain: np.where(class_late, np.where(rain, 0.05, 0.4), np.where(rain, 0.7, 0.9)))
traffic = pm.Bernoulli('traffic', p_traffic, value=values, observed=True)

model = pm.Model([traffic, p_traffic, class_late, p_class_late, rain])

m = pm.MCMC(model)
m.sample(100000)

trace_r = m.trace('rain')[:]
trace_p_class_late = m.trace('p_class_late')[:]
trace_class_late = m.trace('class_late')[:]
trace_p_traffic = m.trace('p_traffic')[:]

frame = {
              'Rain': [1 if ii[0] else 0 for ii in trace_r.tolist() ],
              'class_late': [1 if ii[0] else 0 for ii in trace_class_late.tolist() ],
              'class_late Probability': [ii[0] for ii in trace_p_class_late.tolist()],
              'traffic': [ii[0] for ii in trace_p_traffic.tolist()],
              }
df = pd.DataFrame(frame)

p_rain_class = float(df[(df['Rain'] == 1) & (df['traffic'] > 0.5)].shape[0]) / df[df['traffic'] > 0.5].shape[0] 
print(p_rain_class)