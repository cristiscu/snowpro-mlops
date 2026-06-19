# create a sample of 2500 records for explanation + compute shapley values for each model
# for base model + optimized model - compare

sample=test_pd.rename(columns=rename_dict)
   .sample(n=2500, random_state=100)
   .reset_index(drop=True)

base_shap_pd = mv_base.run(sample, function_name="explain")
opt_shap_pd = mv_opt.run(sample, function_name="explain")

# -------------------------------------------------------------
# visualize feature importance

import shap

# Summary plot for base model
shap.summary_plot(np.array(base_shap_pd.astype(float)), 
      sample.drop(["LOAN_ID","MORTGAGERESPONSE", "TIMESTAMP"], axis=1), 
   feature_names = sample.drop(
      ["LOAN_ID","MORTGAGERESPONSE", "TIMESTAMP"], axis=1).columns)

# Summary plot for optimized model
shap.summary_plot(np.array(opt_shap_pd.astype(float)), 
      sample.drop(["LOAN_ID","MORTGAGERESPONSE", "TIMESTAMP"], axis=1), 
   feature_names = sample.drop(
      ["LOAN_ID","MORTGAGERESPONSE", "TIMESTAMP"], axis=1).columns)

# -------------------------------------------------------------
# analyze feature impact on model predictions

# Merge shap vals and actual vals together for easier plotting
all_shap_base = sample.merge(
   base_shap_pd, right_index=True, left_index=True, how='outer')
all_shap_opt = sample.merge(
   opt_shap_pd, right_index=True, left_index=True, how='outer')

asb_filtered = all_shap_base[(all_shap_base.INCOME>0)
    & (all_shap_base.INCOME<250000)]
aso_filtered = all_shap_opt[(all_shap_opt.INCOME>0)
    & (all_shap_opt.INCOME<250000)]

# Analyze income impact
import seaborn as sns
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(10, 6))

fig.suptitle("INCOME EXPLANATION")
sns.scatterplot(data = asb_filtered, x ='INCOME', 
   y = 'INCOME_explanation', ax=axes[0])
sns.regplot(data = asb_filtered, x = "INCOME", 
   y = 'INCOME_explanation', scatter=False, color='red',
   line_kws = {"lw":2},ci =100, lowess=False, ax =axes[0])

axes[0].set_title('Base Model')
sns.scatterplot(data = aso_filtered, x ='INCOME', 
   y = 'INCOME_explanation',color = "orange", ax = axes[1])
sns.regplot(data = aso_filtered, x = "INCOME", 
   y = 'INCOME_explanation', scatter=False, color='blue',
   line_kws={"lw":2}, ci=100, lowess=False, ax = axes[1])
axes[1].set_title('Opt Model')
plt.show()
