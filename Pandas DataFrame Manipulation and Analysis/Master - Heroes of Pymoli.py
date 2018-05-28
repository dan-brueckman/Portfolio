
# coding: utf-8

# In[124]:


import pandas as pd
import os
csv_file = os.path.join(".", "purchase_data.csv")
heroes = pd.read_csv(csv_file)
heroes_2 = pd.read_csv(csv_file)
heroes_3 = pd.read_csv(csv_file)


# In[125]:


player_count = len(heroes["SN"].unique())
total_players_df = pd.DataFrame({"Total Players": [player_count]})
total_players_df


# In[126]:


item_count = len(heroes["Item ID"].unique())
avg_price = heroes["Price"].mean()
total_purchases = len(heroes.index)
total_revenue = heroes["Price"].sum()
purchasing_analysis_total_df = pd.DataFrame({"Number of Unique Items": [item_count], "Average Purchase Price": [avg_price], "Total Number of Purchases": [total_purchases], "Total Revenue": [total_revenue]})
purchasing_analysis_total_df["Average Purchase Price"] = purchasing_analysis_total_df["Average Purchase Price"].map('${:,.2f}'.format)
purchasing_analysis_total_df["Total Revenue"] = purchasing_analysis_total_df["Total Revenue"].map('${:,.2f}'.format)
purchasing_analysis_total_df


# In[127]:


gender_group = heroes.groupby("Gender")
gender_count_df = pd.DataFrame((gender_group["Gender"].count()/total_purchases)*100).round(2)
gender_count_df["Total Count"] = gender_group["Gender"].count()
gender_count_df = gender_count_df.rename(columns={"Gender": "Percentage of Players"})
gender_count_df


# In[128]:


gender_purchases_df = pd.DataFrame({"Purchase Count": gender_group["Gender"].count(), "Avg Purchase Price": gender_group["Price"].mean(), "Total Purchase Value": gender_group["Price"].sum(), "Normalized Totals": gender_group["Price"].sum()/gender_group["Gender"].count() }).round(2)

gender_purchases_df["Total Purchase Value"] = gender_purchases_df["Total Purchase Value"].map('${:,.2f}'.format)
gender_purchases_df["Normalized Totals"] = gender_purchases_df["Normalized Totals"].map('${:,.2f}'.format)
gender_purchases_df["Avg Purchase Price"] = gender_purchases_df["Avg Purchase Price"].map('${:,.2f}'.format)

gender_purchases_df


# In[129]:


bins = [0,10, 15, 20, 25, 30, 35, 40, 100 ]
group_labels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
heroes["Age Group"] = pd.cut(heroes["Age"], bins, labels=group_labels)

age_group_df = heroes.groupby("Age Group")
age_demo_df = pd.DataFrame((age_group_df["Age Group"].count()/total_purchases)*100).round(2)
age_demo_df["Total Count"] = age_group_df["Age Group"].count()
age_demo_df = age_demo_df.rename(columns={"Age Group": "Percentage of Players"})

age_demo_df


# In[130]:


age_group_summary = pd.DataFrame({"Purchase Count": age_group_df["Age Group"].count(), "Avg Purchase Price": age_group_df["Price"].mean(), "Total Purchase Value": age_group_df["Price"].sum(), "Normalized Totals": age_group_df["Price"].sum()/age_group_df["Age Group"].count() }).round(2)

age_group_summary["Total Purchase Value"] = age_group_summary["Total Purchase Value"].map('${:,.2f}'.format)
age_group_summary["Normalized Totals"] = age_group_summary["Normalized Totals"].map('${:,.2f}'.format)
age_group_summary["Avg Purchase Price"] = age_group_summary["Avg Purchase Price"].map('${:,.2f}'.format)

age_group_summary


# In[131]:


sn_group = heroes.groupby("SN")
sn_group["Price"].sum().nlargest(5)


# In[132]:


heroes_2.set_index("SN", inplace=True)

top_5 = heroes_2.loc[["Undirrala66", "Saedue76", "Mindimnya67", "Haellysu29", "Eoda93"]]

top_group = top_5.groupby("SN")

top_df = pd.DataFrame({"Purchase Count": top_group["Price"].count(), "Average Purchase Price": top_group["Price"].mean(), "Total Purchase Value": top_group["Price"].sum()}).round(2)

top_df["Total Purchase Value"] = top_df["Total Purchase Value"].map('${:,.2f}'.format)
top_df["Average Purchase Price"] = top_df["Average Purchase Price"].map('${:,.2f}'.format)

top_df.sort_values("Total Purchase Value", ascending = False, inplace = True)

top_df 


# In[133]:


item_group = heroes.groupby("Item Name")
item_group["Price"].count().nlargest(10)


# In[134]:


heroes_3.set_index("Item Name", inplace=True)

top_items = heroes_3.loc[["Final Critic", "Arcane Gem", "Betrayal, Whisper of Grieving Widows", "Stormcaller", "Retribution Axe", "Serenity", "Trickster", "Woeful Adamantite Claymore"]]
top_items_group = top_items.groupby(["Item Name", "Item ID"])

items_df = pd.DataFrame({"Purchase Count": top_items_group["Price"].count(), "Total Purchase Value": top_items_group["Price"].sum(), "Item Price":top_items_group["Price"].sum()/top_items_group["Price"].count() })
items_df["Total Purchase Value"] = items_df["Total Purchase Value"].map('${:,.2f}'.format)
items_df["Item Price"] = items_df["Item Price"].map('${:,.2f}'.format)
items_df


# In[135]:


item_group["Price"].sum().nlargest(10)


# In[136]:


top_rev_items = heroes_3.loc[["Final Critic", "Retribution Axe", "Stormcaller", "Spectral Diamond Doomblade", "Orenmir"]]
top_rev_items_gb = top_rev_items.groupby(["Item Name", "Item ID"])

revenue_df = pd.DataFrame({"Purchase Count": top_rev_items_gb["Price"].count(), "Total Purchase Value": top_rev_items_gb["Price"].sum(), "Item Price": top_rev_items_gb["Price"].sum()/top_rev_items_gb["Price"].count() })
revenue_df["Total Purchase Value"] = revenue_df["Total Purchase Value"].map('${:,.2f}'.format)
revenue_df["Item Price"] = revenue_df["Item Price"].map('${:,.2f}'.format)

revenue_df

