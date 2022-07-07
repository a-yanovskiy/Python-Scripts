"""
Script for finding rest of works and materials in estimates and acts.

First argument: takes one main xlsx file - it must contain all the works and materials in full.
Next arguments: takes any number of xlsx files - that contains works and materials in part.

Script merging documents by index, cleans and finds rest of works and materials. 

Returns: xlsx file.
"""

import pandas as pd
import numpy as np
import re


def import_file(path):
    df = pd.read_excel(io=path, engine='openpyxl')
    return df


def define_column_names_by_row(df, column_name, regexp):
    """the first row found that matches the regex condition for the column,
        will become the frame header"""
    for index, row in df.iterrows(): 
        if re.search(regexp, str(row[column_name])):
            return df.rename(columns=df.iloc[index+1]).iloc[index+2:]


def del_nan_rows_in_column(df, column_name):
    """Delete rows where NaN values are in the specified column"""
    return df.dropna(subset=[column_name])


def merge_dfs_by_index(df_1, df_2):
    """combines two frames by index while preserving all rows"""
    return pd.merge(df_1, df_2, left_index=True, right_index=True, how='outer')


def format_table(df):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df.dropna(axis='columns',how='all')
    df = define_column_names_by_row(df, df.columns[0], r'^NN')
    df = del_nan_rows_in_column(df, "2").iloc[:, 0:6]
    df = df.set_index(df.columns[0])
    return df


def merge_tables_to_compare(estimate_path, *acts_path):
    """ attach the last column by index """
    result = format_table(import_file(estimate_path))
    for act_path in acts_path:
        act_number = act_path.rsplit('_', maxsplit=2)[1]
        act = format_table(import_file(act_path)).iloc[:, -2:-1]
        act = act.rename({act.columns[0]: f'акт {act_number}'}, axis='columns')
        result = merge_dfs_by_index(result, act)
        result = result.rename(
            {
                '1': '№ пп',
                '2': 'Код',
                '3': 'Наименование',
                '4': 'изм',
                '5': 'по смете',
                '6': 'Цена',
            },
            axis='columns',
        )
    return result


def main():
    estimate_path = "Smeta.xlsx"
    act_path1 = "Act_1.xlsx"
    act_path2 = "Act_2.xlsx"
    act_path3 = "Act_3.xlsx"
    act_path4 = "Act_4.xlsx"

    t = merge_tables_to_compare(
        estimate_path,
        act_path1,
        act_path2,
        act_path3,
        act_path4,
    )

    with pd.ExcelWriter('result.xlsx') as writer:
        t.to_excel(writer, sheet_name='Comparison')


if __name__ == '__main__':
    main()
