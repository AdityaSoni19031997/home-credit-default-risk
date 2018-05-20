# Copyright 2018 Mamy André-Ratsimbazafy. All rights reserved.

import pandas as pd
import numpy as np
from src.categorical_encoder import encode_categoricals

def fte_family_situation(train, test, y, db_conn, folds, cache_file):
  def _trans(df, table):

    df['name_income_type']    = encode_categoricals(df, db_conn, table, 'NAME_INCOME_TYPE')
    df['name_education_type'] = encode_categoricals(df, db_conn, table, 'NAME_EDUCATION_TYPE')
    df['name_family_status']  = encode_categoricals(df, db_conn, table, 'NAME_FAMILY_STATUS')
    df['name_housing_type']  = encode_categoricals(df, db_conn, table, 'NAME_HOUSING_TYPE')

    query = f"""
    select
      CNT_CHILDREN,
      CNT_FAM_MEMBERS,
      case(CODE_GENDER)
        when "F" THEN 1
        else 0
      end isWoman
    from
      {table}
    ORDER BY
      SK_ID_CURR ASC;
    """
    df[['CNT_CHILDREN', 'CNT_FAM_MEMBERS', 'isWoman']] = pd.read_sql_query(query, db_conn)

  _trans(train, "application_train")
  _trans(test, "application_test")

  return train, test, y, db_conn, folds, cache_file
