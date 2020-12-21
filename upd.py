# -*- coding: utf-8 -*-
import pymysql
from sqlalchemy import create_engine
import getpass
import pandas as pd


password=getpass.getpass()

eng=create_engine(f"mysql+pymysql://root:{password}@localhost/hof")

utd=pd.read_sql_table("six_months", eng)
nutd=pd.read_sql_table("no_update", eng)

# In[2]:
    
TAs=pd.read_sql_table("tas", eng)

#utd.Cohort=utd.Cohort.dt.date

#nutd.Cohort=nutd.Cohort.dt.date
wins=pd.read_sql_table("winners", eng)

wins.to_markdown(index=False)

# In[3]:
    

text=f"""# Ironhack - Hall Of Fame

Below you can find the list of people who became the new versions of themselves here, at Ironhack Paris.
Warm hugs, congrats and thanks for your best performance! All the best and remember that 1% a day keeps unemployment away.

Eldiias.


# Data Analytics bootcamp

{wins.to_markdown(index=False)
}


## Data Paris - Academic Team

{TAs.to_markdown(index=False)}

## Students and their repositories

Below you can find alumni repositories that were updated at least once within the last 6 months. (Including the bootcamp period)

{utd.to_markdown(index=False)}

Below you can find those that were active more than 6 months ago.

{nutd.to_markdown(index=False)}
"""

with open("README.md", "w",encoding="utf-8") as f:
    f.write(text)
